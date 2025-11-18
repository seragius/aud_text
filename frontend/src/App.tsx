import { useState } from 'react'

function App() {
  const [isRecording, setIsRecording] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          VoiceCRM
        </h1>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-semibold mb-4">Grabar Interacción</h2>

          <div className="flex flex-col items-center space-y-4">
            <button
              onClick={() => setIsRecording(!isRecording)}
              className={`w-32 h-32 rounded-full flex items-center justify-center text-white text-2xl font-bold transition-all ${
                isRecording
                  ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                  : 'bg-blue-500 hover:bg-blue-600'
              }`}
            >
              {isRecording ? '⏹' : '🎤'}
            </button>

            <p className="text-gray-600">
              {isRecording ? 'Grabando... Pulsa para detener' : 'Pulsa el micrófono para grabar'}
            </p>
          </div>

          <div className="mt-8 p-4 bg-blue-50 rounded-md">
            <h3 className="font-semibold text-blue-900 mb-2">📋 Próximos pasos:</h3>
            <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
              <li>Instalar dependencias: <code className="bg-blue-100 px-2 py-1 rounded">npm install</code></li>
              <li>Configurar backend en <code className="bg-blue-100 px-2 py-1 rounded">.env</code></li>
              <li>Implementar componentes de React en <code className="bg-blue-100 px-2 py-1 rounded">src/</code></li>
              <li>Ver documentación completa en <code className="bg-blue-100 px-2 py-1 rounded">docs/DEPLOYMENT.md</code></li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
