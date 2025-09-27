import React from 'react';
import { Menu, X, Code, MessageCircle } from 'lucide-react';

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    element?.scrollIntoView({ behavior: 'smooth' });
    setIsMenuOpen(false);
  };

  const openWhatsAppDirect = () => {
    window.open('https://wa.me/5512996182268?text=Olá! Vim do seu site e gostaria de conversar sobre um projeto!', '_blank');
  };

  return (
    <header className="fixed top-0 w-full backdrop-blur-sm border-b z-50" style={{ background: 'hsla(220, 15%, 5%, 0.9)', borderColor: 'hsl(220, 15%, 18%)' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg" style={{ background: 'linear-gradient(45deg, hsl(197, 100%, 50%), hsl(197, 100%, 60%))' }}>
              <Code className="h-6 w-6" style={{ color: 'hsl(220, 15%, 5%)' }} />
            </div>
            <span className="font-bold text-xl" style={{ color: 'hsl(197, 100%, 50%)' }}>DevJS Pro</span>
          </div>

          <nav className="hidden md:flex items-center space-x-8">
            <button onClick={() => scrollToSection('inicio')} className="font-medium transition-colors" style={{ color: 'hsl(197, 100%, 70%)' }} onMouseEnter={(e) => e.target.style.color = 'hsl(197, 100%, 50%)'} onMouseLeave={(e) => e.target.style.color = 'hsl(197, 100%, 70%)'}>
              Início
            </button>
            <button onClick={() => scrollToSection('servicos')} className="font-medium transition-colors" style={{ color: 'hsl(197, 100%, 70%)' }} onMouseEnter={(e) => e.target.style.color = 'hsl(197, 100%, 50%)'} onMouseLeave={(e) => e.target.style.color = 'hsl(197, 100%, 70%)'}>
              Serviços
            </button>
            <button onClick={() => scrollToSection('sobre')} className="font-medium transition-colors" style={{ color: 'hsl(197, 100%, 70%)' }} onMouseEnter={(e) => e.target.style.color = 'hsl(197, 100%, 50%)'} onMouseLeave={(e) => e.target.style.color = 'hsl(197, 100%, 70%)'}>
              Sobre
            </button>
            <button onClick={() => scrollToSection('contato')} className="font-medium transition-colors" style={{ color: 'hsl(197, 100%, 70%)' }} onMouseEnter={(e) => e.target.style.color = 'hsl(197, 100%, 50%)'} onMouseLeave={(e) => e.target.style.color = 'hsl(197, 100%, 70%)'}>
              Contato
            </button>
            <button
              onClick={openWhatsAppDirect}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium flex items-center space-x-2 transition-colors"
            >
              <MessageCircle className="h-4 w-4" />
              <span>WhatsApp</span>
            </button>
          </nav>

          <button
            className="md:hidden p-2"
            style={{ color: 'hsl(197, 100%, 50%)' }}
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {isMenuOpen && (
          <div className="md:hidden border-t py-4" style={{ borderColor: 'hsl(220, 15%, 18%)' }}>
            <nav className="space-y-4">
              <button onClick={() => scrollToSection('inicio')} className="block font-medium" style={{ color: 'hsl(197, 100%, 70%)' }}>
                Início
              </button>
              <button onClick={() => scrollToSection('servicos')} className="block font-medium" style={{ color: 'hsl(197, 100%, 70%)' }}>
                Serviços
              </button>
              <button onClick={() => scrollToSection('sobre')} className="block font-medium" style={{ color: 'hsl(197, 100%, 70%)' }}>
                Sobre
              </button>
              <button onClick={() => scrollToSection('contato')} className="block font-medium" style={{ color: 'hsl(197, 100%, 70%)' }}>
                Contato
              </button>
              <button
                onClick={openWhatsAppDirect}
                className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-3 rounded-lg font-medium flex items-center justify-center space-x-2 transition-colors"
              >
                <MessageCircle className="h-4 w-4" />
                <span>WhatsApp</span>
              </button>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
