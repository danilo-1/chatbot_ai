<template>
  <div class="home container-fluid p-0">
    <!-- Hero Section -->
    <section class="hero d-flex align-items-center justify-content-center text-center bg-primary text-white" style="min-height: 100vh;">
      <div class="container">
        <h1 class="display-4 fw-bold">FastChat</h1>
        <p class="lead mt-4">
          Uma solução rápida e inteligente para conversas com a IA.
        </p>
        <p>
          Utilizando FastAPI, Vue.js e a potência do OpenAI, nossa ferramenta oferece um chat interativo com sugestões inteligentes e suporte a múltiplos modelos.
        </p>
        <router-link to="/chat" class="btn btn-light btn-lg mt-4">Começar Chat</router-link>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features py-5 ">
      <div class="container">
        <h2 class="text-center mb-5">Recursos Inovadores</h2>
        <div class="row">
          <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Resposta Rápida</h5>
                <p class="card-text">
                  Chat em tempo real com respostas geradas pela IA utilizando os modelos mais avançados.
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Sugestões Inteligentes</h5>
                <p class="card-text">
                  Sugestões contextualizadas para ajudar a continuar a conversa de forma autêntica e prática.
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Modo Escuro Integrado</h5>
                <p class="card-text">
                  Interface adaptável com suporte completo para modos claro e escuro, proporcionando a melhor experiência visual.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="row mt-4">
          <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Modelos Customizáveis</h5>
                <p class="card-text">
                  Selecione entre diversos modelos de IA para personalizar a experiência do seu chat.
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Back-end com FastAPI</h5>
                <p class="card-text">
                  Comunicação robusta entre o front-end Vue e o back-end FastAPI para respostas dinâmicas e seguras.
                </p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">Design Responsivo</h5>
                <p class="card-text">
                  Interface intuitiva que se adapta perfeitamente a desktops, tablets e dispositivos móveis.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action Section -->
    <section class="cta py-5 bg-primary text-white text-center">
      <div class="container">
        <h2 class="mb-4">Pronto para experimentar o poder da IA?</h2>
        <router-link to="/chat" class="btn btn-light btn-lg">Iniciar Chat</router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer bg-dark text-white py-3">
      <div class="container text-center">
        <small>© 2025 FastChat. Todos os direitos reservados.</small>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Você pode adicionar lógica adicional aqui se necessário.
</script>

<style scoped>
.hero {
  background-image: url('/src/assets/hero-bg.jpg'); /* insira uma imagem de fundo se desejar */
  background-size: cover;
  background-position: center;
}
.cta {
  /* Ajuste o estilo conforme necessário para harmonizar com o tema */
}
.footer {
  font-size: 0.9rem;
}
</style>