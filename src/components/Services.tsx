import React from 'react';
import { Globe, BarChart3, Cog, Brain, Palette, MessageSquare } from 'lucide-react';

const Services: React.FC = () => {
  const services = [
    { 
      icon: Globe, 
      title: 'Sistemas Web Completos', 
      description: 'Desenvolvimento de aplicações robustas e escaláveis, da interface ao banco de dados, com suporte de IA para otimização, depuração e automação do processo de desenvolvimento.'
    },
    { 
      icon: BarChart3, 
      title: 'Análise e Visualização de Dados', 
      description: 'Criação de dashboards e relatórios inteligentes utilizando JavaScript e Python, com apoio de IA para gerar insights, previsões e modelos de decisão sem depender de ferramentas externas.'
    },
    { 
      icon: Cog, 
      title: 'Automação de Processos', 
      description: 'Integração de APIs, fluxos de vendas, CRM e marketing digital com scripts personalizados, potencializados por IA para identificar padrões e reduzir tarefas manuais.'
    },
    { 
      icon: Brain, 
      title: 'Otimização com IA Aplicada', 
      description: 'Desenvolvimento de soluções inteligentes para marketing, SEO e tomadas de decisão — utilizando IA como aliada estratégica dentro do ecossistema JavaScript e Python.'
    },
    { 
      icon: Palette, 
      title: 'Desenvolvimento com IA Visual', 
      description: 'Criação de sites, aplicativos, jogos, CRMs e materiais digitais com apoio de ferramentas visuais baseadas em IA, que aceleram o design e a prototipagem com resultados profissionais e de alto impacto.'
    },
    { 
      icon: MessageSquare, 
      title: 'Consultoria Técnica', 
      description: 'Orientação especializada para otimização de projetos e implementação de melhores práticas de desenvolvimento, com foco em resultados e eficiência.'
    }
  ];

  return (
    <section id="servicos" className="py-20" style={{ background: 'linear-gradient(135deg, hsl(220, 15%, 5%), hsl(220, 15%, 8%))' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4" style={{ color: 'hsl(197, 100%, 50%)' }}>🚀 O Que Ofereço</h2>
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
                  e.currentTarget.style.borderColor = 'hsl(197, 100%, 50%)';
                  e.currentTarget.style.boxShadow = '0 0 20px hsla(197, 100%, 50%, 0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'hsl(220, 15%, 18%)';
                  e.currentTarget.style.boxShadow = 'none';
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
