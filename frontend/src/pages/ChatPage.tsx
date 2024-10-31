import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  CircularProgress,
  Paper,
  IconButton,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

import 'katex/dist/katex.min.css';

interface Message {
  sender: 'user' | 'assistant';
  text: string;
}

const ChatPage: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to the bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const cleanResponse = (text: string): string => {
    const lines = text.split('\n');
    const uniqueLines = lines.filter(
      (line, index, self) => self.indexOf(line) === index
    );
    return uniqueLines.join('\n');
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setPrompt('');

    const systemPrompt = `
You are a helpful, detail-oriented assistant specialized in providing clear, structured responses with well-commented code examples and formatted mathematical expressions. Follow these guidelines:

1. **Overview**: Start with a brief summary of the solution.
2. **Step-by-Step Instructions**: Use numbered lists or bullet points.
3. **Code Examples**: Provide code examples with consistent indentation, and use comments to explain key parts of the code.
   - Indicate the programming language after the triple backticks. For example, \`\`\`python.
4. **Math and Equations**: Clearly separate each equation and format them using LaTeX-style syntax with display math delimiters ($$...$$) for block equations and $...$ for inline equations.
5. **Readable Formatting**: Use Markdown-style formatting for headings, lists, and code blocks.
6. **Conciseness**: Avoid repetition, and ensure the response is as concise as possible while covering all necessary details.
    `;

    const fullPrompt = `${systemPrompt}\n\nUser: ${prompt}\n\nAssistant:`;

    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: 'user', text: prompt },
    ]);

    try {
      const response = await fetch('http://localhost:8000/v1/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer token-what-a-day`,
        },
        body: JSON.stringify({
          model: 'akjindal53244/Llama-3.1-Storm-8B',
          prompt: fullPrompt,
          max_tokens: 500,
          temperature: 0.7,
          top_p: 0.9,
          repetition_penalty: 1.1,
          presence_penalty: 0.6,
          frequency_penalty: 0.5,
          stream: true,
        }),
      });

      if (!response.body) {
        throw new Error('No response body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let done = false;
      let assistantText = '';

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunkValue = decoder.decode(value);

        const lines = chunkValue.split('\n').filter(Boolean);

        for (const line of lines) {
          const messageLine = line.replace(/^data: /, '').trim();
          if (messageLine === '[DONE]') {
            done = true;
            break;
          }
          try {
            const parsed = JSON.parse(messageLine);
            const text = parsed.choices[0].text;

            assistantText += text;

            const cleanedText = cleanResponse(assistantText);

            setMessages((prevMessages) => {
              const updatedMessages = [...prevMessages];
              if (
                updatedMessages.length > 0 &&
                updatedMessages[updatedMessages.length - 1].sender === 'assistant'
              ) {
                updatedMessages[updatedMessages.length - 1].text = cleanedText;
              } else {
                updatedMessages.push({ sender: 'assistant', text: cleanedText });
              }
              return updatedMessages;
            });
          } catch (e) {
            console.error('Could not parse stream message:', messageLine, e);
          }
        }
      }
    } catch (error) {
      console.error('Error generating response:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'assistant', text: 'Error generating response.' },
      ]);
    }

    setLoading(false);
  };

  const renderMessageContent = (message: Message) => {
    return message.sender === 'assistant' ? (
      <ReactMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          h1: ({ node, ...props }: any) => (
            <Typography
              variant="h5"
              component="h1"
              sx={{
                fontFamily: 'Arial, sans-serif',
                fontWeight: 'bold',
                marginBottom: 1,
              }}
              {...props}
            />
          ),
          h2: ({ node, ...props }: any) => (
            <Typography
              variant="h6"
              component="h2"
              sx={{
                fontFamily: 'Arial, sans-serif',
                fontWeight: 'bold',
                marginBottom: 1,
              }}
              {...props}
            />
          ),
          p: ({ node, ...props }: any) => (
            <Typography
              variant="body1"
              sx={{ fontFamily: 'Arial, sans-serif', marginBottom: 1 }}
              {...props}
            />
          ),
          li: ({ node, ordered, ...props }: any) => (
            <li style={{ marginBottom: 4 }} {...props} />
          ),
          code: ({ node, inline, className, children, ...props }: any) => {
            const match = /language-(\w+)/.exec(className || '');
            const language = match ? match[1] : '';

            // Function to handle copying code to clipboard
            const handleCopy = () => {
              navigator.clipboard.writeText(String(children).replace(/\n$/, ''));
            };

            return !inline ? (
              <Box
                sx={{
                  marginTop: 2,
                  marginBottom: 2,
                  backgroundColor: '#0e0e0e', // Darker background for code block
                  borderRadius: 2,
                  overflow: 'hidden',
                }}
              >
                {/* Header with language name and copy button */}
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    backgroundColor: '#1e1e1e', // Slightly lighter header
                    color: '#fff',
                    padding: '4px 8px',
                  }}
                >
                  <Typography
                    variant="caption"
                    sx={{ fontFamily: 'Arial, sans-serif', fontWeight: 'bold' }}
                  >
                    {language ? language.toUpperCase() : 'CODE'}
                  </Typography>
                  <IconButton
                    size="small"
                    onClick={handleCopy}
                    sx={{ color: '#fff' }}
                    aria-label="Copy code to clipboard"
                  >
                    <ContentCopyIcon fontSize="small" />
                  </IconButton>
                </Box>

                {/* Code block */}
                <SyntaxHighlighter
                  language={language}
                  style={oneDark}
                  customStyle={{
                   margin: 0,
    padding: '16px',
    backgroundColor: '#0e0e0e', // Unified dark background
    color: '#e0e0e0',           // Neutral text color to blend with syntax colors
    fontSize: 14,
    fontFamily: 'Source Code Pro, monospace',
    overflowX: 'auto',
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word',}}
                  PreTag="div"
                  {...props}
                >
                  {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
              </Box>
            ) : (
              <Typography
                component="code"
                sx={{
                  backgroundColor: '#2e2e2e',
                  padding: '2px 4px',
                  borderRadius: '4px',
                  fontFamily: 'Source Code Pro, monospace',
                }}
                {...props}
              >
                {children}
              </Typography>
            );
          },
          blockquote: ({ node, ...props }: any) => (
            <Box
              component="blockquote"
              sx={{
                borderLeft: '4px solid #3f51b5',
                paddingLeft: 2,
                color: '#bbb',
                fontStyle: 'italic',
                marginTop: 1,
                marginBottom: 1,
              }}
              {...props}
            />
          ),
        }}
      >
        {message.text}
      </ReactMarkdown>
    ) : (
      <Typography
        variant="body1"
        sx={{ fontFamily: 'Arial, sans-serif' }}
      >
        {message.text}
      </Typography>
    );
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        height: '100vh',
        padding: 2,
        backgroundColor: '#121212',
      }}
    >
      {/* Conversation Section */}
      <Paper
        elevation={3}
        sx={{
          width: '100%',
          maxWidth: '800px',
          flexGrow: 1,
          padding: 2,
          marginBottom: 2,
          borderRadius: 2,
          backgroundColor: '#1e1e1e',
          overflowY: 'auto',
        }}
      >
        <Typography
          variant="h6"
          gutterBottom
          color="#fff"
          sx={{ fontFamily: 'Arial, sans-serif' }}
        >
          Conversation
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
          {messages.length === 0 && !loading && (
            <Typography color="#bbb" sx={{ fontFamily: 'Arial, sans-serif' }}>
              Your conversation will appear here.
            </Typography>
          )}
          {messages.map((message, index) => (
            <Box
              key={index}
              sx={{
                alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: message.sender === 'user' ? '#3f51b5' : '#2e2e2e',
                color: '#fff',
                borderRadius: 2,
                padding: 1,
                marginBottom: 1,
                maxWidth: '80%',
                wordBreak: 'break-word',
                fontFamily: 'Arial, sans-serif',
                boxShadow: '0px 1px 3px rgba(0,0,0,0.2)',
              }}
            >
              {renderMessageContent(message)}
            </Box>
          ))}
          {loading && (
            <Box
              sx={{
                alignSelf: 'flex-start',
                backgroundColor: '#2e2e2e',
                color: '#fff',
                borderRadius: 2,
                padding: 1,
                marginBottom: 1,
                maxWidth: '80%',
                display: 'flex',
                alignItems: 'center',
              }}
            >
              <Typography variant="body1" sx={{ fontFamily: 'Arial, sans-serif' }}>
                Assistant is typing...
              </Typography>
              <CircularProgress size={20} sx={{ marginLeft: 1 }} />
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>
      </Paper>

      {/* Input Box and Send Button */}
      <Box
        sx={{
          width: '100%',
          maxWidth: '800px',
          padding: 1,
          backgroundColor: '#1e1e1e',
          borderRadius: 2,
          boxShadow: '0px 1px 3px rgba(0,0,0,0.2)',
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <TextField
            fullWidth
            variant="outlined"
            label="Enter your prompt..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleGenerate();
              }
            }}
            multiline
            minRows={1}
            maxRows={4}
            sx={{
              marginRight: 2,
              '& .MuiOutlinedInput-root': {
                backgroundColor: '#2e2e2e',
                color: '#fff',
                '& fieldset': {
                  borderColor: '#3f51b5',
                },
                '&:hover fieldset': {
                  borderColor: '#3f51b5',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#3f51b5',
                },
              },
              '& .MuiInputLabel-root': {
                color: '#bbb',
              },
              '& .MuiInputLabel-root.Mui-focused': {
                color: '#3f51b5',
              },
              '& .MuiInputBase-input': {
                fontFamily: 'Arial, sans-serif',
              },
            }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleGenerate}
            endIcon={<SendIcon />}
            disabled={loading}
            sx={{
              backgroundColor: '#3f51b5',
              color: '#fff',
              '&:hover': {
                backgroundColor: '#303f9f',
              },
              fontFamily: 'Arial, sans-serif',
            }}
          >
            Send
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default ChatPage;

