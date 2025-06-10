import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { audioBookService } from './services/api';

interface Audiobook {
  id: number;
  title: string;
  status: string;
  audio_url?: string;
  created_at: string;
  progress?: number;
  current_step?: number;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [audiobooks, setAudiobooks] = useState<Audiobook[]>([]);
  const [selectedAudiobook, setSelectedAudiobook] = useState<Audiobook | null>(null);
  const [processingStatus, setProcessingStatus] = useState<string>('');
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Novos estados para entrada de texto
  const [inputMode, setInputMode] = useState<'file' | 'text'>('file');
  const [textInput, setTextInput] = useState('');
  const [titleInput, setTitleInput] = useState('');

  // Refs para evitar manipulação direta do DOM
  const playerSectionRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const isMountedRef = useRef(true);

  // Carregar audiobooks ao iniciar
  useEffect(() => {
    loadAudiobooks();
    // Atualizar lista a cada 30 segundos
    const interval = setInterval(loadAudiobooks, 30000);
    return () => clearInterval(interval);
  }, []);

  // Cleanup ao desmontar componente
  useEffect(() => {
    return () => {
      // Marcar como desmontado
      isMountedRef.current = false;
      // Limpar estados ao desmontar
      setUploading(false);
      setProcessingStatus('');
      setProgress(0);
    };
  }, []);

  const loadAudiobooks = async () => {
    try {
      const data = await audioBookService.getAudiobooks();
      // Ordenar por ID decrescente (mais recentes primeiro)
      setAudiobooks(data.sort((a: Audiobook, b: Audiobook) => b.id - a.id));
    } catch (error) {
      console.error('Erro ao carregar audiobooks:', error);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const resetFileInput = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleDeleteAudiobook = async (audiobook: Audiobook) => {
    const confirmDelete = window.confirm(
      `Tem certeza que deseja deletar o audiobook "${audiobook.title}"?\n\nEsta ação não pode ser desfeita e removerá todos os arquivos associados.`
    );
    
    if (!confirmDelete) return;
    
    try {
      await audioBookService.deleteAudiobook(audiobook.id);
      
      // Se o audiobook deletado era o selecionado, limpar seleção
      if (selectedAudiobook && selectedAudiobook.id === audiobook.id) {
        setSelectedAudiobook(null);
      }
      
      // Recarregar lista
      await loadAudiobooks();
      
      alert(`Audiobook "${audiobook.title}" deletado com sucesso!`);
    } catch (error) {
      console.error('Erro ao deletar audiobook:', error);
      alert('Erro ao deletar audiobook. Tente novamente.');
    }
  };

  const handleDeleteAllAudiobooks = async () => {
    if (audiobooks.length === 0) {
      alert('Não há audiobooks para deletar.');
      return;
    }
    
    const confirmDeleteAll = window.confirm(
      `Tem certeza que deseja deletar TODOS os ${audiobooks.length} audiobooks?\n\nEsta ação não pode ser desfeita e removerá todos os arquivos associados.`
    );
    
    if (!confirmDeleteAll) return;
    
    try {
      // Deletar todos os audiobooks
      const deletePromises = audiobooks.map(audiobook => 
        audioBookService.deleteAudiobook(audiobook.id)
      );
      
      await Promise.all(deletePromises);
      
      // Limpar seleção
      setSelectedAudiobook(null);
      
      // Recarregar lista
      await loadAudiobooks();
      
      alert('Todos os audiobooks foram deletados com sucesso!');
    } catch (error) {
      console.error('Erro ao deletar audiobooks:', error);
      alert('Erro ao deletar alguns audiobooks. Verifique a lista e tente novamente.');
    }
  };

  const handleUpload = async () => {
    if (inputMode === 'file') {
      if (!file) {
        alert('Por favor, selecione um arquivo!');
        return;
      }
      await processFile();
    } else {
      if (!textInput.trim()) {
        alert('Por favor, digite o texto!');
        return;
      }
      if (!titleInput.trim()) {
        alert('Por favor, digite um título!');
        return;
      }
      if (textInput.trim().length < 10) {
        alert('O texto deve ter pelo menos 10 caracteres!');
        return;
      }
      await processText();
    }
  };

  const processFile = async () => {
    setUploading(true);
    setProcessingStatus('📤 Enviando arquivo...');
    setProgress(0);

    try {
      const response = await audioBookService.uploadFile(file!);
      
      // 🐛 FIX: Verificar se o audiobook já está pronto (processamento síncrono)
      if (response.status === 'completed') {
        // Audiobook já está pronto!
        setProcessingStatus('✅ Audiobook criado com sucesso!');
        setProgress(100);
        setSelectedAudiobook(response);
        loadAudiobooks();
        
        // Limpar formulários
        resetFileInput();
        setUploading(false);
        
        // Scroll para o player
        setTimeout(() => {
          if (isMountedRef.current) {
            playerSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
          }
        }, 500);
      } else {
        // Processamento assíncrono - monitorar status
        setProcessingStatus('🎵 Gerando narração com IA...');
        await monitorProcessing(response.id);
      }
      
    } catch (error) {
      console.error('Erro ao fazer upload:', error);
      setProcessingStatus('❌ Erro ao fazer upload do arquivo');
      setUploading(false);
    }
  };

  const processText = async () => {
    setUploading(true);
    setProcessingStatus('📝 Processando texto...');
    setProgress(0);

    try {
      const response = await audioBookService.createFromText(titleInput.trim(), textInput.trim());
      
      // 🐛 FIX: Verificar se o audiobook já está pronto (processamento síncrono)
      if (response.status === 'completed') {
        // Audiobook já está pronto!
        setProcessingStatus('✅ Audiobook criado com sucesso!');
        setProgress(100);
        setSelectedAudiobook(response);
        loadAudiobooks();
        
        // Limpar formulários
        setTextInput('');
        setTitleInput('');
        setUploading(false);
        
        // Scroll para o player
        setTimeout(() => {
          if (isMountedRef.current) {
            playerSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
          }
        }, 500);
      } else {
        // Processamento assíncrono - monitorar status
        setProcessingStatus('🎵 Gerando narração com IA...');
        await monitorProcessing(response.id);
      }
      
    } catch (error) {
      console.error('Erro ao processar texto:', error);
      setProcessingStatus('❌ Erro ao processar texto');
      setUploading(false);
    }
  };

  const monitorProcessing = async (audiobookId: number) => {
    // Timeout de segurança - liberar botão após 5 minutos
    const safetyTimeout = setTimeout(() => {
      if (isMountedRef.current) {
        setUploading(false);
        setProcessingStatus('⚠️ Tempo limite excedido. Verifique a lista de audiobooks.');
      }
    }, 5 * 60 * 1000); // 5 minutos

    // Verificar status do processamento
    const checkStatus = setInterval(async () => {
      try {
        // Verificar se o componente ainda está montado
        if (!isMountedRef.current) {
          clearInterval(checkStatus);
          return;
        }

        const status = await audioBookService.getAudiobookStatus(audiobookId);
        
        if (!isMountedRef.current) {
          clearInterval(checkStatus);
          return;
        }
        
        if (status.status === 'completed') {
          clearInterval(checkStatus);
          clearTimeout(safetyTimeout);
          if (isMountedRef.current) {
            setProcessingStatus('✅ Audiobook criado com sucesso!');
            setProgress(100);
            const audiobook = await audioBookService.getAudiobook(audiobookId);
            setSelectedAudiobook(audiobook);
            loadAudiobooks();
            
            // Limpar formulários
            if (inputMode === 'file') {
              resetFileInput();
            } else {
              setTextInput('');
              setTitleInput('');
            }
            
            setUploading(false);
            
            // Scroll para o player
            setTimeout(() => {
              if (isMountedRef.current) {
                playerSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
              }
            }, 500);
          }
        } else if (status.status === 'error') {
          clearInterval(checkStatus);
          clearTimeout(safetyTimeout);
          if (isMountedRef.current) {
            setProcessingStatus(`❌ Erro: ${status.error}`);
            setUploading(false);
          }
        } else {
          if (isMountedRef.current) {
            const progressValue = status.progress || 0;
            setProgress(progressValue);
            const steps = ['📄 Extraindo texto', '🎭 Analisando conteúdo', '🎤 Gerando narração', '🎵 Adicionando música', '💾 Salvando arquivo'];
            const currentStep = status.current_step || 0;
            setProcessingStatus(`${steps[currentStep] || 'Processando...'} (${progressValue}%)`);
          }
        }
      } catch (error) {
        console.error('Erro ao verificar status:', error);
        if (isMountedRef.current) {
          clearInterval(checkStatus);
          clearTimeout(safetyTimeout);
          setUploading(false); // 🐛 FIX: Limpar estado de upload em caso de erro
          setProcessingStatus('❌ Erro ao verificar status do processamento');
        }
      }
    }, 2000);
  };

  const getStatusBadge = (status: string) => {
    const statusMap: { [key: string]: { label: string; class: string; icon: string } } = {
      'completed': { label: 'Completo', class: 'completed', icon: '✅' },
      'processing': { label: 'Processando', class: 'processing', icon: '⏳' },
      'error': { label: 'Erro', class: 'error', icon: '❌' }
    };
    
    const statusInfo = statusMap[status] || { label: status, class: 'default', icon: '📄' };
    
    return (
      <span className={`status-badge ${statusInfo.class}`}>
        {statusInfo.icon} {statusInfo.label}
      </span>
    );
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🎧 Sistema de Audiobook com IA</h1>
        <p>Transforme seus textos em audiobooks narrados com voz natural e música de fundo</p>
      </header>

      <main className="main-container">
        {/* Card de Upload */}
        <div className="upload-card">
          <h2>📤 Criar Audiobook</h2>
          
          {/* Notificação sobre melhorias */}
          <div style={{
            background: 'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
            color: 'white',
            padding: '0.75rem 1rem',
            borderRadius: '8px',
            marginBottom: '1rem',
            border: '1px solid rgba(255,255,255,0.2)',
            fontSize: '0.9rem'
          }}>
            <strong>✨ Sistema Totalmente Melhorado!</strong><br/>
            ✅ Textos grandes processados com Google Cloud TTS (sem soletração)<br/>
            ✅ Nomes próprios pronunciados corretamente (ex: "Kanzime" → "Canzimi")<br/>
            ✅ Qualidade máxima de áudio para qualquer tamanho de texto
          </div>
          
          {/* Toggle entre File Upload e Text Input */}
          <div style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            marginBottom: '1.5rem',
            gap: '1rem'
          }}>
            <button
              onClick={() => setInputMode('file')}
              className={`toggle-button ${inputMode === 'file' ? 'active' : ''}`}
              style={{
                padding: '0.5rem 1rem',
                border: '2px solid #667eea',
                borderRadius: '8px',
                background: inputMode === 'file' ? '#667eea' : 'transparent',
                color: inputMode === 'file' ? 'white' : '#667eea',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
            >
              📁 Upload de Arquivo
            </button>
            <button
              onClick={() => setInputMode('text')}
              className={`toggle-button ${inputMode === 'text' ? 'active' : ''}`}
              style={{
                padding: '0.5rem 1rem',
                border: '2px solid #667eea',
                borderRadius: '8px',
                background: inputMode === 'text' ? '#667eea' : 'transparent',
                color: inputMode === 'text' ? 'white' : '#667eea',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
            >
              ✍️ Digitar Texto
            </button>
          </div>

          {/* Modo Upload de Arquivo */}
          {inputMode === 'file' && (
            <div>
              <div 
                className="drop-zone" 
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="drop-zone-icon">📁</div>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.pdf,.docx"
                  onChange={handleFileChange}
                  disabled={uploading}
                  style={{ display: 'none' }}
                />
                <h3>Clique aqui para selecionar um arquivo</h3>
                <p>Formatos aceitos: TXT, PDF, DOCX</p>
                
                {file && (
                  <div style={{ 
                    marginTop: '1rem', 
                    padding: '1rem', 
                    background: 'rgba(102, 126, 234, 0.1)', 
                    borderRadius: '8px',
                    border: '1px solid rgba(102, 126, 234, 0.3)'
                  }}>
                    <strong>📄 {file.name}</strong>
                    <br />
                    <small>{(file.size / 1024).toFixed(2)} KB</small>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Modo Entrada de Texto */}
          {inputMode === 'text' && (
            <div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ 
                  display: 'block', 
                  marginBottom: '0.5rem', 
                  fontWeight: 'bold',
                  color: '#333'
                }}>
                  📝 Título do Audiobook:
                </label>
                <input
                  type="text"
                  value={titleInput}
                  onChange={(e) => setTitleInput(e.target.value)}
                  placeholder="Digite o título do seu audiobook..."
                  disabled={uploading}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '2px solid #e1e5e9',
                    borderRadius: '8px',
                    fontSize: '1rem',
                    outline: 'none',
                    transition: 'border-color 0.3s ease'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#667eea'}
                  onBlur={(e) => e.target.style.borderColor = '#e1e5e9'}
                />
              </div>
              
              <div>
                <label style={{ 
                  display: 'block', 
                  marginBottom: '0.5rem', 
                  fontWeight: 'bold',
                  color: '#333'
                }}>
                  📖 Texto do Capítulo:
                </label>
                <textarea
                  ref={textareaRef}
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder="Cole ou digite aqui o texto do seu capítulo...&#10;&#10;Exemplo:&#10;Era uma vez, em uma terra muito distante..."
                  disabled={uploading}
                  rows={12}
                  style={{
                    width: '100%',
                    padding: '1rem',
                    border: '2px solid #e1e5e9',
                    borderRadius: '8px',
                    fontSize: '1rem',
                    fontFamily: 'inherit',
                    resize: 'vertical',
                    minHeight: '200px',
                    outline: 'none',
                    transition: 'border-color 0.3s ease'
                  }}
                  onFocus={(e) => e.target.style.borderColor = '#667eea'}
                  onBlur={(e) => e.target.style.borderColor = '#e1e5e9'}
                />
                <div style={{ 
                  textAlign: 'right', 
                  marginTop: '0.5rem', 
                  fontSize: '0.9rem', 
                  color: '#666' 
                }}>
                  {textInput.length} caracteres
                </div>
              </div>
            </div>
          )}
          
          <button 
            onClick={handleUpload} 
            disabled={
              uploading || 
              (inputMode === 'file' && !file) || 
              (inputMode === 'text' && (!textInput.trim() || !titleInput.trim()))
            }
            className="upload-button"
          >
            {uploading ? (
              <>
                <span className="loading-spinner"></span>
                Processando...
              </>
            ) : (
              <>🚀 Gerar Audiobook</>
            )}
          </button>
          
          {processingStatus && (
            <div key="processing-status" className="progress-container">
              <p>{processingStatus}</p>
              {uploading && (
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Player de Áudio */}
        {selectedAudiobook && selectedAudiobook.audio_url && (
          <div ref={playerSectionRef} className="audio-player">
            <h3>🎵 Audiobook Pronto!</h3>
            <h4>{selectedAudiobook.title}</h4>
            <audio 
              controls 
              src={selectedAudiobook.audio_url}
              style={{ width: '100%', marginTop: '1rem' }}
              autoPlay
            />
            <div className="action-buttons" style={{ marginTop: '1rem' }}>
              <a 
                href={selectedAudiobook.audio_url} 
                download={`${selectedAudiobook.title}.mp3`}
                className="action-button download-button"
              >
                📥 Baixar MP3
              </a>
            </div>
          </div>
        )}

        {/* Lista de Audiobooks */}
        <div className="upload-card" style={{ marginTop: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2>📚 Meus Audiobooks ({audiobooks.length})</h2>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button 
                onClick={loadAudiobooks}
                className="action-button"
                style={{ padding: '0.5rem 1rem' }}
              >
                🔄 Atualizar
              </button>
              {audiobooks.length > 0 && (
                <button 
                  onClick={handleDeleteAllAudiobooks}
                  className="action-button"
                  style={{ 
                    padding: '0.5rem 1rem',
                    backgroundColor: '#ff4757',
                    borderColor: '#ff4757'
                  }}
                >
                  🗑️ Deletar Todos
                </button>
              )}
            </div>
          </div>
          
          {audiobooks.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">📚</div>
              <p>Nenhum audiobook criado ainda</p>
              <small>Faça upload de um arquivo para começar!</small>
            </div>
          ) : (
            <div className="audiobook-grid">
              {audiobooks.map((audiobook) => (
                <div key={audiobook.id} className="audiobook-card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                    <h4>{audiobook.title}</h4>
                    {getStatusBadge(audiobook.status)}
                  </div>
                  
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>
                    ID: #{audiobook.id}
                  </p>
                  
                  <p style={{ color: '#666', fontSize: '0.9rem' }}>
                    📅 {new Date(audiobook.created_at).toLocaleString('pt-BR')}
                  </p>

                  <div className="action-buttons">
                    {audiobook.audio_url && (
                      <>
                        <button 
                          onClick={() => setSelectedAudiobook(audiobook)}
                          className="action-button play-button"
                        >
                          ▶️ Reproduzir
                        </button>
                        <a
                          href={audiobook.audio_url}
                          download={`${audiobook.title}.mp3`}
                          className="action-button download-button"
                        >
                          📥 Baixar
                        </a>
                      </>
                    )}
                    <button
                      onClick={() => handleDeleteAudiobook(audiobook)}
                      className="action-button delete-button"
                      style={{
                        backgroundColor: '#ff4757',
                        borderColor: '#ff4757',
                        marginLeft: audiobook.audio_url ? '0.5rem' : '0'
                      }}
                    >
                      🗑️ Deletar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Botão flutuante de upload */}
      <button
        className="fab-button"
        onClick={() => {
          if (inputMode === 'file') {
            fileInputRef.current?.click();
          } else {
            // Focar no campo de texto
            textareaRef.current?.focus();
          }
        }}
        disabled={uploading}
        style={{
          position: 'fixed',
          bottom: '2rem',
          right: '2rem',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          border: 'none',
          color: 'white',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 4px 20px rgba(102, 126, 234, 0.4)',
          transition: 'transform 0.3s ease',
        }}
        onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
        title={inputMode === 'file' ? 'Selecionar arquivo' : 'Focar no campo de texto'}
      >
        {inputMode === 'file' ? '📤' : '✍️'}
      </button>
    </div>
  );
}

export default App; 