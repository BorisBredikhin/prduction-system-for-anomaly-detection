import { Dispatch, SetStateAction } from "react";

function generate() {
    return 541
}

export class Client {
    public readonly client_id: number
    ws: WebSocket;
    messages?: HTMLDivElement
 
    receivedMessage(ev: MessageEvent<any>) {
        this.messages!.innerHTML+=`<p>${ev.data}</p>`
    }
    
    constructor() {
        this.client_id = generate()
        this.ws = new WebSocket(`ws://localhost:8000/ws/${this.client_id}`)
        this.ws.onmessage = (ev) => this.receivedMessage(ev)
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
            console.log(query)
            this1.ws.send(JSON.stringify({
                action: "query",
                client_id: this1.client_id,
                query: query
            }))
            searchQuery.value = ""
        }
    }
}
