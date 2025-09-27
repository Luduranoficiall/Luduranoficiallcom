import React from 'react';
import { Code, Heart } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="border-t" style={{ background: 'hsl(220, 15%, 5%)', borderColor: 'hsl(220, 15%, 18%)', color: 'hsl(197, 100%, 50%)' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center text-center md:text-left">
          <div className="mb-4 md:mb-0">
            <p style={{ color: 'hsl(197, 100%, 70%)' }}>
              © {new Date().getFullYear()} DevJS Pro. Todos os direitos reservados.
            </p>
            <p className="text-sm" style={{ color: 'hsl(197, 100%, 50%)' }}>Desenvolvedor Full-Stack JavaScript | Harvard & FIAP</p>
          </div>
          <div className="flex items-center space-x-2" style={{ color: 'hsl(197, 100%, 70%)' }}>
            <span>Feito com</span>
            <Heart className="h-5 w-5 text-red-500" />
            <span>e</span>
            <div className="p-1.5 rounded" style={{ background: 'linear-gradient(45deg, hsl(197, 100%, 50%), hsl(197, 100%, 60%))' }}>
              <Code className="h-4 w-4 text-white" />
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
