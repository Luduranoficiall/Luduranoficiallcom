import React from 'react';
import { GraduationCap, Award, Users, TrendingUp } from 'lucide-react';

const About: React.FC = () => {
  const highlights = [
    { icon: GraduationCap, title: 'Formação de Excelência', description: 'Harvard (Ciência da Computação) e FIAP (Engenharia de Software).' },
    { icon: Award, title: 'Stack Unificada', description: 'Menos complexidade e mais resultados com JavaScript e Python.' },
    { icon: Users, title: 'Foco em Resultados', description: 'Sistemas que resolvem problemas e impulsionam sua receita.' },
    { icon: TrendingUp, title: 'IA Integrada', description: 'Inteligência artificial para maior eficiência e inovação no seu projeto.' }
  ];

  return (
    <section id="sobre" className="py-20" style={{ background: 'linear-gradient(135deg, hsl(220, 15%, 5%), hsl(220, 15%, 8%))' }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold mb-6" style={{ color: 'hsl(197, 100%, 50%)' }}>Por Que Escolher Meus Serviços?</h2>
            <p className="text-lg mb-8 leading-relaxed" style={{ color: 'hsl(197, 100%, 70%)' }}>
              Combino o rigor acadêmico de Harvard e FIAP para entregar inovação com aplicabilidade real. Garanto agilidade, coerência técnica e manutenção simplificada.
            </p>
            <div className="p-6 rounded-xl border" style={{ background: 'hsla(197, 100%, 50%, 0.1)', borderColor: 'hsl(220, 15%, 18%)', color: 'hsl(197, 100%, 50%)' }}>
              <h3 className="text-xl font-semibold mb-3">🚀 Tecnologia simplificada. Resultados extraordinários.</h3>
              <p style={{ color: 'hsl(197, 100%, 70%)' }}>
                Contrate um desenvolvedor full-stack que unifica tecnologia e resultados.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {highlights.map((highlight) => {
              const IconComponent = highlight.icon;

              return (
                <div key={highlight.title} className="border rounded-xl p-6" style={{ background: 'hsl(220, 15%, 12%)', borderColor: 'hsl(220, 15%, 18%)' }}>
                  <div className="w-12 h-12 rounded-lg flex items-center justify-center mb-4" style={{ background: 'hsla(197, 100%, 50%, 0.1)' }}>
                    <IconComponent className="h-6 w-6" style={{ color: 'hsl(197, 100%, 50%)' }} />
                  </div>
                  <h3 className="text-lg font-semibold mb-2" style={{ color: 'hsl(197, 100%, 50%)' }}>{highlight.title}</h3>
                  <p className="text-sm leading-relaxed" style={{ color: 'hsl(197, 100%, 70%)' }}>{highlight.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
