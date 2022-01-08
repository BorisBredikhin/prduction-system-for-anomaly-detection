import { Dispatch, SetStateAction } from "react";

function generate(): number {
    return Math.floor(Math.random() * 100)
}

export type Message ={
    form: "user" | "ai"
    text: string
}

export class Client {
    public readonly client_id: number
    ws: WebSocket;
    setMessages: Dispatch<SetStateAction<Message[]>>;
    messages: Message[];
 
    receivedMessage(msg: string, fromUser: boolean) {
        this.messages.push({form: fromUser? 'user':'ai', text: msg})
        var msgs = document.getElementById('msgs')!
        msgs.innerHTML = this.messages.map(m=>`<div class="message ${m.form}"><p>${m.text}</p></div>`).join('')
        msgs.scrollTop = msgs.scrollHeight - msgs.clientHeight
    }
    
    constructor(messages: Message[], setMessages: Dispatch<SetStateAction<Message[]>>) {
        this.client_id = generate()
        this.ws = new WebSocket(`ws://localhost:8000/ws/${this.client_id}`)
        this.ws.onmessage = (ev) => this.receivedMessage(ev.data, false)
        this.messages = messages
        this.setMessages = setMessages
    }

    async connect() {
        await this.ws.send(JSON.stringify({
            action: "connected",
            client_id: this.client_id
        }))
    }

    sendQuery(searchQueryId: string, messagesId: string) {
        const this1 = this
        return function () {
           let searchQuery = document.getElementById(searchQueryId)! as HTMLInputElement
           this1.messages = this1.messages ?? document.getElementById(messagesId) as HTMLDivElement

            const query = searchQuery.value
            this1.receivedMessage(query, true)
            this1.ws.send(JSON.stringify({
                action: "query",
                client_id: this1.client_id,
                query: query
            }))
            searchQuery.value = ""
        }
    }
}
