import React, { useState, useRef, useEffect } from "react";
import {
  Send,
  Bot,
  User,
  Search,
  Database,
  Brain,
  Zap,
  MessageCircle,
  Sparkles,
} from "lucide-react";

import ReactMarkdown from 'react-markdown'

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

const TechSymbol = ({
  icon: Icon,
  className = "",
  delay = 0,
}: {
  icon: any;
  className?: string;
  delay?: number;
}) => (
  <div
    className={`absolute opacity-5 animate-pulse ${className}`}
    style={{ animationDelay: `${delay}s` }}
  >
    <Icon size={48} />
  </div>
);

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Welcome to Docs Nexus! I'm your semantic search assistant. I can help you find information across your documentation using natural language queries. What would you like to search for?",
      isUser: false,
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const apiUrl = import.meta.env.VITE_API_URL;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setIsTyping(true);
    try {
      const response = await fetch(
        `${apiUrl}/assistant?query=${inputText}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.message,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
    setIsTyping(false);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 relative overflow-hidden">
      {/* Background Tech Symbols */}
      <div className="absolute inset-0 pointer-events-none">
        <TechSymbol icon={Database} className="top-20 left-20" delay={0} />
        <TechSymbol icon={Brain} className="top-40 right-32" delay={1} />
        <TechSymbol icon={Search} className="bottom-40 left-40" delay={2} />
        <TechSymbol icon={Zap} className="bottom-20 right-20" delay={3} />
        <TechSymbol icon={Database} className="top-60 left-60" delay={4} />
        <TechSymbol icon={Brain} className="top-80 right-80" delay={5} />
        <TechSymbol icon={Sparkles} className="bottom-60 right-60" delay={6} />
        <TechSymbol icon={MessageCircle} className="top-32 left-80" delay={7} />
      </div>

      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200/50 shadow-sm relative z-10">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-xl">
                <Search className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Docs-Nexus
                </h1>
                <p className="text-sm text-gray-600">
                  Semantic Search Assistant
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>Pandas</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="max-w-4xl mx-auto px-6 py-6 flex flex-col h-[calc(100vh-88px)]">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto space-y-4 mb-6 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start space-x-3 animate-fade-in ${
                message.isUser ? "flex-row-reverse space-x-reverse" : ""
              }`}
            >
              <div
                className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                  message.isUser
                    ? "bg-gradient-to-r from-blue-500 to-blue-600"
                    : "bg-gradient-to-r from-purple-500 to-purple-600"
                }`}
              >
                {message.isUser ? (
                  <User className="w-5 h-5 text-white" />
                ) : (
                  <Bot className="w-5 h-5 text-white" />
                )}
              </div>
              <div
                className={`flex-1 max-w-2xl ${
                  message.isUser ? "flex justify-end" : ""
                }`}
              >
                <div
                  className={`px-4 py-3 rounded-2xl shadow-sm ${
                    message.isUser
                      ? "bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-br-md"
                      : "bg-white/80 backdrop-blur-sm text-gray-800 rounded-bl-md border border-gray-100"
                  }`}
                >
                  <div className="prose prose-sm max-w-none text-sm leading-relaxed">
                    <ReactMarkdown>
                      {message.text}
                    </ReactMarkdown>
                  </div>
                  <p
                    className={`text-xs mt-2 ${
                      message.isUser ? "text-blue-100" : "text-gray-500"
                    }`}
                  >
                    {formatTime(message.timestamp)}
                  </p>
                </div>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex items-start space-x-3 animate-fade-in">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-r from-purple-500 to-purple-600 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-white/80 backdrop-blur-sm px-4 py-3 rounded-2xl rounded-bl-md border border-gray-100 shadow-sm">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  ></div>
                  <div
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-200/50 shadow-lg p-4">
          <form
            onSubmit={handleSendMessage}
            className="flex items-center space-x-3"
          >
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Ask me anything about your documentation..."
                className="w-full px-4 py-3 bg-gray-50/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder-gray-500"
                disabled={isTyping}
              />
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <Search className="w-4 h-4 text-gray-400" />
              </div>
            </div>
            <button
              type="submit"
              disabled={!inputText.trim() || isTyping}
              className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400 text-white p-3 rounded-xl transition-all duration-200 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed shadow-lg"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <div className="flex items-center justify-between mt-3 text-xs text-gray-500">
            <div className="flex items-center space-x-4">
              <span>Powered by semantic search</span>
              <div className="flex items-center space-x-1">
                <div className="w-1 h-1 bg-gray-300 rounded-full"></div>
                <span>AI-driven documentation discovery</span>
              </div>
            </div>
            <div className="text-gray-400">Press Enter to send</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
