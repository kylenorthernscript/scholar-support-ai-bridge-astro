import React, { useState } from 'react';

interface PreScreeningData {
  age?: string;
  gender?: string;
  location?: string;
  researchTypes?: string[];
  language?: string;
  availability?: string;
}

interface PreScreeningFlowProps {
  onComplete: (data: PreScreeningData) => void;
  currentStep: number;
}

export const PreScreeningFlow: React.FC<PreScreeningFlowProps> = ({ onComplete, currentStep }) => {
  const [formData, setFormData] = useState<PreScreeningData>({});

  const researchTypeOptions = [
    { id: 'online-survey', label: 'オンライン調査', icon: '💻' },
    { id: 'interview', label: '対面インタビュー', icon: '🗣️' },
    { id: 'experiment', label: '実験参加', icon: '🔬' },
    { id: 'focus-group', label: 'フォーカスグループ', icon: '👥' },
  ];

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">基本情報</h3>
            <div className="grid gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">年齢</label>
                <input
                  type="number"
                  placeholder="例: 25"
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">性別</label>
                <select
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                >
                  <option value="">選択してください</option>
                  <option value="male">男性</option>
                  <option value="female">女性</option>
                  <option value="other">その他</option>
                  <option value="prefer-not-to-say">回答しない</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">お住まいの地域</label>
                <input
                  type="text"
                  placeholder="例: 東京都"
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                />
              </div>
            </div>
          </div>
        );
      
      case 2:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">参加可能な研究形式</h3>
            <p className="text-sm text-gray-600">該当するものをすべて選択してください</p>
            <div className="grid grid-cols-2 gap-3">
              {researchTypeOptions.map((option) => (
                <label
                  key={option.id}
                  className="flex cursor-pointer items-center space-x-3 rounded-lg border border-gray-300 p-3 hover:border-blue-500 hover:bg-blue-50"
                >
                  <input
                    type="checkbox"
                    value={option.id}
                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    onChange={(e) => {
                      const types = formData.researchTypes || [];
                      if (e.target.checked) {
                        setFormData({ ...formData, researchTypes: [...types, option.id] });
                      } else {
                        setFormData({ ...formData, researchTypes: types.filter(t => t !== option.id) });
                      }
                    }}
                  />
                  <span className="text-xl">{option.icon}</span>
                  <span className="text-sm font-medium text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">言語・参加可能時間</h3>
            <div className="grid gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">対応可能な言語</label>
                <select
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                >
                  <option value="">選択してください</option>
                  <option value="japanese">日本語</option>
                  <option value="english">英語</option>
                  <option value="chinese">中国語</option>
                  <option value="spanish">スペイン語</option>
                  <option value="french">フランス語</option>
                  <option value="other">その他</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">参加可能な時間帯</label>
                <select
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  onChange={(e) => setFormData({ ...formData, availability: e.target.value })}
                >
                  <option value="">選択してください</option>
                  <option value="weekday-morning">平日午前</option>
                  <option value="weekday-afternoon">平日午後</option>
                  <option value="weekday-evening">平日夜間</option>
                  <option value="weekend">週末</option>
                  <option value="flexible">柔軟に対応可能</option>
                </select>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="rounded-lg bg-blue-50 p-4">
      {renderStep()}
      <div className="mt-4 flex justify-end">
        <button
          onClick={() => onComplete(formData)}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          次へ
        </button>
      </div>
    </div>
  );
};