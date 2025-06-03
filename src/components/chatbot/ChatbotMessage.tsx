import React from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: any;
}

interface ChatbotMessageProps {
  message: Message;
}

export const ChatbotMessage: React.FC<ChatbotMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-white shadow-sm ring-1 ring-gray-200'
        }`}
      >
        {!isUser && (
          <div className="mb-1 flex items-center space-x-2">
            <div className="h-6 w-6 rounded-full bg-gradient-to-r from-blue-600 to-blue-700 p-1">
              <svg className="h-full w-full text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <span className="text-xs font-medium text-gray-600">アシスタント</span>
          </div>
        )}
        <p className={`whitespace-pre-wrap text-sm ${isUser ? '' : 'text-gray-700'}`}>
          {message.content}
        </p>
        <p className={`mt-1 text-xs ${isUser ? 'text-blue-100' : 'text-gray-400'}`}>
          {message.timestamp.toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  );
};