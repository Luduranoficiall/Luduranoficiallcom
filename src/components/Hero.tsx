import React from 'react';
import { ArrowRight, Zap, Shield, Trophy, MessageCircle, Star } from 'lucide-react';

const Hero: React.FC = () => {
  const scrollToContact = () => {
    document.getElementById('contato')?.scrollIntoView({ behavior: 'smooth' });
  };

  const openWhatsAppDirect = () => {
    window.open('https://wa.me/5512996182268?text=Olá! Tenho um projeto e gostaria de conversar urgente!', '_blank');
  };

  return (
    <section id="inicio" className="pt-24 md:pt-32 relative overflow-hidden" style={{ background: 'linear-gradient(135deg, hsl(220, 15%, 5%), hsl(220, 15%, 8%))' }}>
      {/* Background Effects */}
      <div className="absolute inset-0" style={{ background: 'linear-gradient(135deg, hsla(197, 100%, 50%, 0.03), hsla(220, 15%, 5%, 1), hsla(197, 100%, 50%, 0.03))' }}></div>
      <div className="absolute top-1/4 left-1/4 w-72 h-72 rounded-full blur-3xl" style={{ background: 'hsla(197, 100%, 50%, 0.05)' }}></div>
      <div className="absolute bottom-1/4 right-1/4 w-72 h-72 rounded-full blur-3xl" style={{ background: 'hsla(197, 100%, 50%, 0.05)' }}></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="animate-fade-in-up">
            <div className="flex items-center space-x-2 mb-6">
              <span className="bg-gradient-to-r from-green-500 to-emerald-400 text-black px-4 py-2 rounded-full text-sm font-bold">
                ✨ DISPONÍVEL AGORA
              </span>
              <div className="flex items-center space-x-1">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                ))}
                <span className="text-sm ml-2" style={{ color: 'hsl(197, 100%, 70%)' }}>5.0 ⭐ Avaliação</span>
              </div>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight" style={{ color: 'hsl(197, 100%, 50%)' }}>
              Desenvolvedor 
              <span className="bg-gradient-to-r from-cyan-300 via-blue-300 to-cyan-400 bg-clip-text text-transparent animate-gradient-x"> Full-Stack </span>
              JavaScript
            </h1>

            <p className="text-xl mb-8 leading-relaxed" style={{ color: 'hsl(197, 100%, 70%)' }}>
              Formado em <strong style={{ color: 'hsl(197, 100%, 50%)', backgroundColor: 'hsla(197, 100%, 50%, 0.1)', padding: '4px 8px', borderRadius: '4px' }}>Ciência da Computação pela Harvard</strong> e <strong style={{ color: 'hsl(197, 100%, 50%)', backgroundColor: 'hsla(197, 100%, 50%, 0.1)', padding: '4px 8px', borderRadius: '4px' }}>Engenharia de Software pela FIAP</strong>. 
              Crio soluções completas em JavaScript com integração de IA para resultados extraordinários.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 mb-8">
              <button 
                onClick={openWhatsAppDirect}
                className="group bg-gradient-to-r from-green-600 to-green-500 hover:from-green-500 hover:to-green-400 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-2xl shadow-green-500/25 hover:shadow-green-400/40 transform hover:scale-105 transition-all duration-300 flex items-center justify-center space-x-3"
              >
                <MessageCircle className="h-6 w-6 group-hover:animate-bounce" />
                <span>CHAMAR NO WHATSAPP</span>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-ping"></div>
              </button>
              <button 
                onClick={scrollToContact}
                className="group px-8 py-4 rounded-xl font-bold text-lg transition-all duration-300 flex items-center justify-center space-x-3"
                style={{ 
                  border: `2px solid hsl(197, 100%, 50%)`,
                  color: 'hsl(197, 100%, 50%)'
                }}
                onMouseEnter={(e) => {
                  e.target.style.backgroundColor = 'hsla(197, 100%, 50%, 0.1)';
                  e.target.style.color = 'hsl(197, 100%, 70%)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.backgroundColor = 'transparent';
                  e.target.style.color = 'hsl(197, 100%, 50%)';
                }}
              >
                <span>Ver Detalhes</span>
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>

            <div className="grid grid-cols-3 gap-6">
              <div className="text-center group cursor-pointer">
                <div className="p-3 rounded-xl border transition-colors" style={{ background: 'hsla(197, 100%, 50%, 0.1)', borderColor: 'hsl(220, 15%, 18%)' }}>
                  <Zap className="h-8 w-8 mx-auto mb-2 group-hover:animate-pulse" style={{ color: 'hsl(197, 100%, 50%)' }} />
                </div>
                <p className="text-sm font-bold group-hover:text-blue-400 transition-colors" style={{ color: 'hsl(197, 100%, 70%)' }}>Stack Unificada</p>
              </div>
              <div className="text-center group cursor-pointer">
                <div className="p-3 rounded-xl border transition-colors" style={{ background: 'hsla(197, 100%, 50%, 0.1)', borderColor: 'hsl(220, 15%, 18%)' }}>
                  <Shield className="h-8 w-8 mx-auto mb-2 group-hover:animate-pulse" style={{ color: 'hsl(197, 100%, 50%)' }} />
                </div>
                <p className="text-sm font-bold group-hover:text-blue-400 transition-colors" style={{ color: 'hsl(197, 100%, 70%)' }}>IA Integrada</p>
              </div>
              <div className="text-center group cursor-pointer">
                <div className="p-3 rounded-xl border transition-colors" style={{ background: 'hsla(197, 100%, 50%, 0.1)', borderColor: 'hsl(220, 15%, 18%)' }}>
                  <Trophy className="h-8 w-8 mx-auto mb-2 group-hover:animate-pulse" style={{ color: 'hsl(197, 100%, 50%)' }} />
                </div>
                <p className="text-sm font-bold group-hover:text-blue-400 transition-colors" style={{ color: 'hsl(197, 100%, 70%)' }}>Harvard + FIAP</p>
              </div>
            </div>
          </div>

          <div className="relative animate-fade-in-up animation-delay-300">
            <div className="absolute inset-0 rounded-3xl blur-xl" style={{ background: 'hsla(197, 100%, 50%, 0.1)' }}></div>
            <div className="relative backdrop-blur-sm border rounded-3xl p-8 transition-colors" style={{ background: 'hsla(220, 15%, 12%, 0.8)', borderColor: 'hsl(220, 15%, 18%)', color: 'hsl(197, 100%, 50%)' }}>
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-bold" style={{ color: 'hsl(197, 100%, 50%)' }}>Tecnologias Principais</h3>
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="border rounded-xl p-4 transition-colors group" style={{ background: 'hsla(220, 15%, 8%, 0.6)', borderColor: 'hsl(220, 15%, 18%)' }}>
                  <h4 className="font-bold mb-2 group-hover:text-blue-300" style={{ color: 'hsl(197, 100%, 50%)' }}>Frontend</h4>
                  <p className="text-sm" style={{ color: 'hsl(197, 100%, 70%)' }}>React, TS, Tailwind</p>
                </div>
                <div className="border rounded-xl p-4 transition-colors group" style={{ background: 'hsla(220, 15%, 8%, 0.6)', borderColor: 'hsl(220, 15%, 18%)' }}>
                  <h4 className="font-bold mb-2 group-hover:text-blue-300" style={{ color: 'hsl(197, 100%, 50%)' }}>Backend</h4>
                  <p className="text-sm" style={{ color: 'hsl(197, 100%, 70%)' }}>Node.js, APIs</p>
                </div>
                <div className="border rounded-xl p-4 transition-colors group" style={{ background: 'hsla(220, 15%, 8%, 0.6)', borderColor: 'hsl(220, 15%, 18%)' }}>
                  <h4 className="font-bold mb-2 group-hover:text-blue-300" style={{ color: 'hsl(197, 100%, 50%)' }}>Dados</h4>
                  <p className="text-sm" style={{ color: 'hsl(197, 100%, 70%)' }}>Python, Analytics</p>
                </div>
                <div className="border rounded-xl p-4 transition-colors group" style={{ background: 'hsla(220, 15%, 8%, 0.6)', borderColor: 'hsl(220, 15%, 18%)' }}>
                  <h4 className="font-bold mb-2 group-hover:text-blue-300" style={{ color: 'hsl(197, 100%, 50%)' }}>IA</h4>
                  <p className="text-sm" style={{ color: 'hsl(197, 100%, 70%)' }}>Automação, ML</p>
                </div>
              </div>
              
              <button
                onClick={openWhatsAppDirect}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white py-4 px-6 rounded-xl font-bold text-lg flex items-center justify-center space-x-3 transition-all duration-300 transform hover:scale-105 shadow-lg shadow-blue-500/25"
              >
                <span>SABER MAIS</span>
                <ArrowRight className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
