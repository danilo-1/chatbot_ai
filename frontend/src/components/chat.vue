<template>
    <div class="container mt-5">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h3>Chatbot (FastAPI + Vue.js)</h3>
            </div>
            <div class="card-body chat-container">
                <div 
                    v-for="(msg, index) in messages" 
                    :key="index" 
                    :class="['message', msg.role === 'user' ? 'user-message' : 'bot-message']"
                >
                    <strong>{{ msg.role === 'user' ? 'Você' : 'Bot' }}:</strong> {{ msg.content }}
                </div>
            </div>
            <div class="card-footer">
                <div class="input-group">
                    <input 
                        v-model="userInput" 
                        @keyup.enter="sendMessage"
                        class="form-control"
                        placeholder="Digite sua mensagem..."
                        :disabled="isLoading"
                    />
                    <button 
                        @click="sendMessage" 
                        class="btn btn-primary"
                        :disabled="isLoading || !userInput.trim()"
                    >
                        <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
                        Enviar
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useChatStore } from '@/stores/chat';
import { mapState, mapActions } from 'pinia';

export default {
    computed: {
        ...mapState(useChatStore, ['messages', 'userInput', 'isLoading']),
    },
    methods: {
        ...mapActions(useChatStore, ['sendMessage']),
    },
};
</script>

<style scoped>
.chat-container {
    height: 400px;
    overflow-y: auto;
    padding: 10px;
    background-color: #f8f9fa;
}

.message {
    padding: 8px 12px;
    margin: 5px;
    border-radius: 8px;
    max-width: 80%;
}

.user-message {
    background-color: #007bff;
    color: white;
    margin-left: auto;
    text-align: right;
}

.bot-message {
    background-color: #e9ecef;
    margin-right: auto;
}
</style>