import logo from './logo.svg';
import './App.css';

function App() {
  const startGoogleLogin = () => {
    // inicia fluxo no backend; backend responderá com redirect para o Google
    window.location.href = '/api/auth/google/login/';
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Bem-vindo ao fórum — agora com opção de login social.
        </p>

        <div style={{marginTop: 12}}>
          <button onClick={startGoogleLogin} style={{padding: '10px 16px', borderRadius: 6, background: '#4285F4', color: '#fff', border: 'none', cursor: 'pointer'}}>
            Login com Google
          </button>
        </div>

        <p style={{marginTop: 10, fontSize: 12}}>O botão acima inicia o fluxo OAuth2. Configure `GOOGLE_CLIENT_ID` e `GOOGLE_REDIRECT_URI` no backend para que o fluxo funcione.</p>

      </header>
    </div>
  );
}

export default App;
