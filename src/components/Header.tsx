import { useState, useEffect } from 'react';
import ThemeToggle from './ThemeToggle';

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
        <div className="flex items-center justify-between h-16 md:h-18">
          <div className="flex items-center space-x-3">
            <div className="relative w-10 h-10 bg-slate-800 rounded-lg shadow-lg overflow-hidden">
              {/* Orange accent line */}
              <div className="absolute top-0 left-0 w-full h-1 bg-orange-500"></div>
              
              {/* Content area */}
              <div className="flex items-center justify-center h-full">
                <span className="text-white font-bold text-lg font-serif">θ</span>
              </div>
              
              {/* Subtle grid pattern */}
              <div className="absolute inset-0 opacity-10">
                <div className="grid grid-cols-3 gap-0.5 h-full p-1">
                  <div className="bg-white rounded-sm"></div>
                  <div className="bg-white rounded-sm"></div>
                  <div className="bg-white rounded-sm"></div>
                </div>
              </div>
            </div>
            <span className="text-lg md:text-xl font-bold text-foreground">
              <span className="hidden sm:inline">Theta Clinical Support</span>
              <span className="sm:hidden">Theta</span>
            </span>
          </div>
          
          <nav className="hidden md:flex items-center space-x-8">
            <button 
              onClick={() => scrollToSection('services')}
              className="text-muted-foreground hover:text-primary transition-colors font-medium"
            >
              サービス内容
            </button>
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
            <ThemeToggle />
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