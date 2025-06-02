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
        <div className="flex items-center justify-between h-18">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl shadow-lg"></div>
            <span className="text-xl font-bold text-foreground">Research Support AI</span>
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
          
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            <button 
              onClick={() => scrollToSection('contact')}
              className="btn-primary text-sm px-6 py-3"
            >
              無料相談
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;