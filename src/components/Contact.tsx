import React from 'react';
import { MessageCircle, Send, CheckCircle, Clock, Zap } from 'lucide-react';

const Contact: React.FC = () => {
  const [formData, setFormData] = React.useState({ name: '', email: '', project: '', message: '' });
  const [isSubmitted, setIsSubmitted] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const whatsappMessage = `🚀 *NOVO PROJETO*\n\n👤 *Nome:* ${formData.name}\n📧 *Email:* ${formData.email}\n💼 *Tipo:* ${formData.project}\n\n💬 *Mensagem:*\n${formData.message}\n\n_Enviado pelo site profissional_`;
    const encodedMessage = encodeURIComponent(whatsappMessage);
    window.open(`https://wa.me/5512996182268?text=${encodedMessage}`, '_blank');
    
    setIsLoading(false);
    setIsSubmitted(true);
    setFormData({ name: '', email: '', project: '', message: '' });
    setTimeout(() => setIsSubmitted(false), 3000);
  };

  const openWhatsAppDirect = () => {
    window.open('https://wa.me/5512996182268?text=🚨 *PROJETO URGENTE* 🚨%0A%0AOlá! Vim do seu site e tenho um projeto que precisa ser desenvolvido com urgência. Vamos conversar?', '_blank');
  };

  return (
    <section id="contato" className="py-20 relative overflow-hidden" style={{ background: 'linear-gradient(135deg, hsl(220, 15%, 5%), hsl(220, 15%, 8%))' }}>
      {/* Background Effects */}
      <div className="absolute inset-0" style={{ background: 'linear-gradient(to top, hsla(220, 15%, 12%, 0.2), hsl(220, 15%, 5%))' }}></div>
      <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-96 h-96 rounded-full blur-3xl" style={{ background: 'hsla(197, 100%, 50%, 0.05)' }}></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-bold mb-4" style={{ color: 'hsl(197, 100%, 50%)' }}>
            Pronto para 
            <span className="bg-gradient-to-r from-cyan-300 to-blue-400 bg-clip-text text-transparent"> Começar</span>?
          </h2>
          <p className="text-xl max-w-3xl mx-auto" style={{ color: 'hsl(197, 100%, 70%)' }}>Entre em contato agora para transformar sua ideia em realidade.</p>
        </div>

        <div className="max-w-5xl mx-auto">
          {/* Urgency Banner */}
          <div className="border rounded-2xl p-6 mb-8 text-center" style={{ background: 'hsla(0, 70%, 50%, 0.1)', borderColor: 'hsl(0, 70%, 50%)' }}>
            <div className="flex items-center justify-center space-x-3 mb-3">
              <Zap className="h-6 w-6 text-yellow-400 animate-pulse" />
              <h3 className="text-2xl font-bold" style={{ color: 'hsl(197, 100%, 50%)' }}>🚨 ATENDIMENTO URGENTE</h3>
              <Zap className="h-6 w-6 text-yellow-400 animate-pulse" />
            </div>
            <p className="text-lg" style={{ color: 'hsl(197, 100%, 70%)' }}>
              <Clock className="inline h-5 w-5 mr-2 text-green-400" />
              Resposta garantida em <strong className="text-green-400">5 minutos</strong> no WhatsApp!
            </p>
          </div>

          <div className="backdrop-blur-sm border rounded-3xl p-8 shadow-2xl" style={{ background: 'hsla(220, 15%, 12%, 0.6)', borderColor: 'hsl(220, 15%, 18%)' }}>
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Contact Info */}
              <div className="text-center lg:text-left">
                <div className="flex items-center justify-center lg:justify-start space-x-3 mb-4">
                  <div className="w-4 h-4 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-green-400 font-bold text-lg">ONLINE AGORA</span>
                </div>
                
                <h3 className="text-3xl font-bold mb-4" style={{ color: 'hsl(197, 100%, 50%)' }}>Contato Direto e Urgente</h3>
                <p className="mb-6 text-lg leading-relaxed" style={{ color: 'hsl(197, 100%, 70%)' }}>
                  Para uma resposta imediata, clique no botão abaixo e fale comigo diretamente no WhatsApp. 
                  <strong className="text-green-400"> Resposta garantida em 5 minutos!</strong>
                </p>
                
                <button
                  onClick={openWhatsAppDirect}
                  className="group w-full bg-gradient-to-r from-green-600 via-green-500 to-emerald-500 hover:from-green-500 hover:via-green-400 hover:to-emerald-400 text-white px-8 py-5 rounded-2xl font-bold text-xl flex items-center justify-center space-x-4 transform hover:scale-105 transition-all duration-300 shadow-2xl shadow-green-500/30 hover:shadow-green-400/50 relative overflow-hidden"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                  <MessageCircle className="h-7 w-7 group-hover:animate-bounce relative z-10" />
                  <span className="relative z-10">CHAMAR NO WHATSAPP</span>
                  <div className="absolute -top-2 -right-2 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-xs font-bold">!</span>
                  </div>
                </button>
              </div>

              {/* Form */}
              <div className="relative">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="relative">
                      <input 
                        type="text" 
                        name="name" 
                        required 
                        value={formData.name}
                        onChange={handleInputChange} 
                        className="w-full px-4 py-4 border rounded-xl focus:ring-2 focus:border-transparent transition-all duration-300" 
                        style={{ 
                          background: 'hsla(220, 15%, 5%, 0.6)', 
                          borderColor: 'hsl(220, 15%, 18%)', 
                          color: 'hsl(197, 100%, 50%)'
                        }}
                        placeholder="Seu Nome Completo *" 
                      />
                    </div>
                    <div className="relative">
                      <input 
                        type="email" 
                        name="email" 
                        required 
                        value={formData.email}
                        onChange={handleInputChange} 
                        className="w-full px-4 py-4 border rounded-xl focus:ring-2 focus:border-transparent transition-all duration-300" 
                        style={{ 
                          background: 'hsla(220, 15%, 5%, 0.6)', 
                          borderColor: 'hsl(220, 15%, 18%)', 
                          color: 'hsl(197, 100%, 50%)'
                        }}
                        placeholder="Seu Melhor Email *" 
                      />
                    </div>
                  </div>
                  
                  <div>
                    <select 
                      name="project" 
                      required 
                      value={formData.project}
                      onChange={handleInputChange} 
                      className="w-full px-4 py-4 border rounded-xl focus:ring-2 focus:border-transparent transition-all duration-300"
                      style={{ 
                        background: 'hsla(220, 15%, 5%, 0.6)', 
                        borderColor: 'hsl(220, 15%, 18%)', 
                        color: 'hsl(197, 100%, 50%)'
                      }}
                    >
                      <option value="">Tipo de Projeto *</option>
                      <option value="Site/Landing Page">🌐 Site/Landing Page</option>
                      <option value="Sistema Web Completo">💻 Sistema Web Completo</option>
                      <option value="Automação/IA">🤖 Automação/IA</option>
                      <option value="Análise de Dados">📊 Análise de Dados</option>
                      <option value="Consultoria">💡 Consultoria</option>
                      <option value="Projeto Urgente">🚨 PROJETO URGENTE</option>
                    </select>
                  </div>
                  
                  <div>
                    <textarea 
                      name="message" 
                      required 
                      rows={4} 
                      value={formData.message}
                      onChange={handleInputChange} 
                      className="w-full px-4 py-4 border rounded-xl focus:ring-2 focus:border-transparent transition-all duration-300 resize-none" 
                      style={{ 
                        background: 'hsla(220, 15%, 5%, 0.6)', 
                        borderColor: 'hsl(220, 15%, 18%)', 
                        color: 'hsl(197, 100%, 50%)'
                      }}
                      placeholder="Descreva seu projeto detalhadamente... Quanto mais informações, melhor posso ajudar! *"
                    ></textarea>
                  </div>
                  
                  <button
                    type="submit"
                    disabled={isLoading || isSubmitted}
                    className="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:from-gray-600 disabled:to-gray-500 text-white py-4 px-6 rounded-xl font-bold text-lg transition-all duration-300 flex items-center justify-center space-x-3 transform hover:scale-105 shadow-lg shadow-blue-500/25"
                  >
                    {isLoading ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                        <span>Enviando...</span>
                      </>
                    ) : isSubmitted ? (
                      <>
                        <CheckCircle className="h-5 w-5" />
                        <span>Enviado com Sucesso!</span>
                      </>
                    ) : (
                      <>
                        <Send className="h-5 w-5" />
                        <span>Enviar para WhatsApp</span>
                      </>
                    )}
                  </button>
                </form>
                
                {isSubmitted && (
                  <div className="absolute inset-0 bg-green-500/10 backdrop-blur-sm rounded-xl flex items-center justify-center">
                    <div className="bg-green-600 text-white px-6 py-3 rounded-xl font-bold flex items-center space-x-2">
                      <CheckCircle className="h-6 w-6" />
                      <span>Redirecionando para WhatsApp...</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
