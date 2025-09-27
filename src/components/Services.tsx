import React from 'react';
import { Globe, BarChart3, Cog, Brain, Palette, Rocket } from 'lucide-react';

const Services: React.FC = () => {
  const services = [
    { icon: Globe, title: 'Sistemas Web Completos', description: 'Aplicações robustas e escaláveis, 100% em JavaScript com suporte de IA.' },
    { icon: BarChart3, title: 'Análise de Dados', description: 'Dashboards e relatórios inteligentes utilizando JavaScript e Python.' },
    { icon: Cog, title: 'Automação de Processos', description: 'Integração de APIs, funis de vendas e fluxos de marketing com scripts.' },
    { icon: Brain, title: 'Otimização com IA', description: 'Soluções de IA para marketing, SEO e tomada de decisões estratégicas.' },
    { icon: Palette, title: 'Desenvolvimento Canva IA', description: 'Criação de apps, sites e CRMs utilizando a plataforma visual Canva IA.' },
    { icon: Rocket, title: 'Consultoria Técnica', description: 'Orientação especializada para otimização de projetos e melhores práticas.' }
  ];

  return (
    <section id="servicos" className="py-20" style={{ background: 'linear-gradient(135deg, hsl(220, 15%, 5%), hsl(220, 15%, 8%))' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4" style={{ color: 'hsl(197, 100%, 50%)' }}>O Que Ofereço?</h2>
          <p className="text-xl max-w-3xl mx-auto" style={{ color: 'hsl(197, 100%, 70%)' }}>
            Soluções completas em JavaScript e Python com a vantagem estratégica de uma stack unificada.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service) => {
            const IconComponent = service.icon;
            
            return (
              <div 
                key={service.title} 
                className="border rounded-xl p-6 transition-all duration-300 hover:shadow-lg" 
                style={{ 
                  background: 'hsl(220, 15%, 12%)', 
                  borderColor: 'hsl(220, 15%, 18%)',
                  boxShadow: 'none'
                }}
                onMouseEnter={(e) => {
                  e.target.style.borderColor = 'hsl(197, 100%, 50%)';
                  e.target.style.boxShadow = '0 0 20px hsla(197, 100%, 50%, 0.1)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.borderColor = 'hsl(220, 15%, 18%)';
                  e.target.style.boxShadow = 'none';
                }}
              >
                <div className="w-12 h-12 rounded-lg flex items-center justify-center mb-4" style={{ background: 'hsla(197, 100%, 50%, 0.1)' }}>
                  <IconComponent className="h-6 w-6" style={{ color: 'hsl(197, 100%, 50%)' }} />
                </div>
                <h3 className="text-xl font-semibold mb-3" style={{ color: 'hsl(197, 100%, 50%)' }}>{service.title}</h3>
                <p className="leading-relaxed" style={{ color: 'hsl(197, 100%, 70%)' }}>{service.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Services;
