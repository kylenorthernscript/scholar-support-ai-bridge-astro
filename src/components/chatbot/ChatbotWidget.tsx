import React, { useState, useRef, useEffect } from 'react';
import { ChatbotMessage } from './ChatbotMessage';
import { ChatbotInput } from './ChatbotInput';
import { PreScreeningFlow } from './PreScreeningFlow';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: {
    stage?: 'greeting' | 'prescreening' | 'qualification' | 'scheduling';
    formData?: any;
  };
}

export const ChatbotWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'こんにちは！Theta Clinical Supportのリサーチ参加アシスタントです。\n\n臨床研究への参加をご検討いただき、ありがとうございます。24時間365日、いつでもご相談をお受けしています。\n\nどのような研究への参加をご希望ですか？',
      timestamp: new Date(),
      metadata: { stage: 'greeting' }
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [currentStage, setCurrentStage] = useState<'greeting' | 'prescreening' | 'qualification' | 'scheduling'>('greeting');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: getAIResponse(content, currentStage),
        timestamp: new Date(),
        metadata: { stage: currentStage }
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const getAIResponse = (userInput: string, stage: string): string => {
    // This is a simplified response logic - in production, this would call an AI API
    if (stage === 'greeting') {
      setCurrentStage('prescreening');
      return `承知いたしました。まず、基本的な参加条件を確認させていただきます。\n\n以下の情報をお教えください：\n1. 年齢\n2. 性別\n3. 現在お住まいの地域\n4. 参加可能な研究形式（オンライン調査/対面インタビュー/実験参加）`;
    } else if (stage === 'prescreening') {
      return `ありがとうございます。お客様の条件に合う研究をAIマッチングシステムで検索しています...\n\n現在、以下の研究で参加者を募集しています：\n- オンライン調査（所要時間：30分、謝礼：3,000円）\n- 対面インタビュー（所要時間：60分、謝礼：8,000円）\n\nご興味のある研究はございますか？`;
    }
    return '申し訳ございません。もう一度お聞かせください。';
  };

  return (
    <>
      {/* Floating button - Enhanced visibility */}
      <div className={`fixed bottom-6 right-6 z-50 ${isOpen ? 'scale-0' : 'scale-100'} transition-all`}>
        {/* Pulsing ring effect */}
        <div className="absolute inset-0 h-16 w-16 animate-ping rounded-full bg-blue-400 opacity-75"></div>
        <div className="absolute inset-0 h-16 w-16 animate-ping rounded-full bg-blue-400 opacity-50" style={{ animationDelay: '0.5s' }}></div>
        
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="relative flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-2xl transition-all hover:scale-110 hover:shadow-blue-500/50"
          aria-label="チャットサポートを開く"
        >
          <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          
          {/* Badge for "DEMO" */}
          <span className="absolute -top-1 -right-1 flex h-8 w-8">
            <span className="relative inline-flex rounded-full h-8 w-8 bg-yellow-500 text-gray-900 text-xs font-bold items-center justify-center">
              DEMO
            </span>
          </span>
        </button>
        
        {/* Tooltip */}
        <div className="absolute bottom-20 right-0 bg-gray-900 text-white text-sm px-3 py-2 rounded-lg whitespace-nowrap shadow-lg animate-bounce">
          <div className="absolute bottom-0 right-6 transform translate-y-1/2 rotate-45 w-2 h-2 bg-gray-900"></div>
          🎯 AIチャットボットのデモを体験
        </div>
      </div>

      {/* Chat window */}
      <div
        className={`fixed bottom-6 right-6 z-50 flex h-[600px] w-[400px] flex-col overflow-hidden rounded-lg bg-white shadow-2xl transition-all ${
          isOpen ? 'scale-100 opacity-100' : 'scale-0 opacity-0'
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between bg-gradient-to-r from-blue-600 to-blue-700 p-4 text-white">
          <div className="flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white/20">
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold">リサーチ参加アシスタント (デモ)</h3>
              <p className="text-xs text-blue-100">カスタマイズ可能なAIチャットボット</p>
            </div>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="rounded-full p-1 hover:bg-white/20"
            aria-label="チャットを閉じる"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Messages area */}
        <div className="flex-1 overflow-y-auto bg-gray-50 p-4">
          <div className="space-y-4">
            {messages.map((message) => (
              <ChatbotMessage key={message.id} message={message} />
            ))}
            {isTyping && (
              <div className="flex items-center space-x-2 text-gray-500">
                <div className="flex space-x-1">
                  <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" />
                  <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '0.1s' }} />
                  <div className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '0.2s' }} />
                </div>
                <span className="text-sm">入力中...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input area */}
        <ChatbotInput onSendMessage={handleSendMessage} />
      </div>
    </>
  );
};