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
      isScrolled ? 'backdrop-blur-glass shadow-lg' : 'bg-transparent'
    }`}>
      <div className="container-custom">
        <div className="flex items-center justify-between h-20 md:h-24">
          <a href="/" className="flex items-center space-x-3 md:space-x-4 hover:opacity-80 transition-opacity">
            <img 
              src="/logo.png" 
              alt="Theta Clinical Support Logo" 
              className="w-14 h-14 md:w-20 md:h-20"
            />
            <span className="text-base sm:text-lg md:text-xl font-bold text-foreground">
              <span className="hidden sm:inline">Theta Clinical Support</span>
              <span className="sm:hidden">Theta Clinical Support</span>
            </span>
          </a>
          
          <nav className="hidden md:flex items-center space-x-6">
            <div className="relative group">
              <button className="text-muted-foreground hover:text-primary transition-colors font-medium flex items-center">
                サービス
                <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute top-full left-0 mt-2 w-56 bg-white rounded-lg shadow-lg py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                <a href="/medical-translation" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  医療翻訳・通訳サービス
                </a>
                <a href="/research-recruitment" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  日本在住外国人リクルート
                </a>
                <div className="border-t border-gray-200 my-2"></div>
                <button 
                  onClick={() => scrollToSection('services')}
                  className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  サービス一覧
                </button>
              </div>
            </div>
            <button 
              onClick={() => scrollToSection('features')}
              className="text-muted-foreground hover:text-primary transition-colors font-medium"
            >
              選ばれる理由
            </button>
            <button 
              onClick={() => scrollToSection('faq')}
              className="text-muted-foreground hover:text-primary transition-colors font-medium"
            >
              よくある質問
            </button>
            <button 
              onClick={() => scrollToSection('company')}
              className="text-muted-foreground hover:text-primary transition-colors font-medium"
            >
              会社情報
            </button>
          </nav>
          
          <div className="flex items-center space-x-2 md:space-x-4">
            <button 
              onClick={() => scrollToSection('contact')}
              className="btn-primary text-xs md:text-sm px-3 py-2 md:px-6 md:py-3"
            >
              <span className="hidden sm:inline">無料相談</span>
              <span className="sm:hidden">相談</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;