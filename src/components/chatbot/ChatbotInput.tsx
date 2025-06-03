import React, { useState, useRef } from 'react';

interface ChatbotInputProps {
  onSendMessage: (message: string) => void;
}

export const ChatbotInput: React.FC<ChatbotInputProps> = ({ onSendMessage }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (input.trim()) {
      onSendMessage(input.trim());
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="flex items-end space-x-2">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInput}
          onKeyPress={handleKeyPress}
          placeholder="メッセージを入力..."
          className="max-h-32 min-h-[40px] flex-1 resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          rows={1}
        />
        <button
          onClick={handleSubmit}
          disabled={!input.trim()}
          className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600 text-white transition-colors hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          aria-label="送信"
        >
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
      <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
        <span>Shift + Enter で改行</span>
        <span>研究倫理を遵守した安全な通信</span>
      </div>
    </div>
  );
};