import { useState, useEffect } from 'react';

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white/95 backdrop-blur-md shadow-sm' : 'bg-transparent'
    }`}>
      <div className="container-custom">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg"></div>
            <span className="text-lg font-bold text-gray-900">Research Support AI</span>
          </div>
          
          <nav className="hidden md:flex items-center space-x-8">
            <button 
              onClick={() => scrollToSection('services')}
              className="text-gray-600 hover:text-primary-600 transition-colors"
            >
              サービス内容
            </button>
            <button 
              onClick={() => scrollToSection('features')}
              className="text-gray-600 hover:text-primary-600 transition-colors"
            >
              選ばれる理由
            </button>
            <button 
              onClick={() => scrollToSection('faq')}
              className="text-gray-600 hover:text-primary-600 transition-colors"
            >
              よくある質問
            </button>
            <button 
              onClick={() => scrollToSection('company')}
              className="text-gray-600 hover:text-primary-600 transition-colors"
            >
              会社情報
            </button>
          </nav>
          
          <button 
            onClick={() => scrollToSection('contact')}
            className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md transition-colors"
          >
            無料相談
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;