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
          <div className="flex items-center space-x-3 md:space-x-4">
            <img 
              src="/logo.png" 
              alt="Theta Clinical Support Logo" 
              className="w-14 h-14 md:w-20 md:h-20"
            />
            <span className="text-base sm:text-lg md:text-xl font-bold text-foreground">
              <span className="hidden sm:inline">Theta Clinical Support</span>
              <span className="sm:hidden">Theta Clinical Support</span>
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