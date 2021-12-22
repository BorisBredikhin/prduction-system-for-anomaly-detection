function generate() {
    return 541
}

export class Client {
    public readonly client_id: number
    ws: WebSocket;

    constructor() {
        this.client_id = generate()
        this.ws = new WebSocket(`ws://localhost:8000/ws/${this.client_id}`)
    }

    async connect() {
        await this.ws.send(JSON.stringify({
            action: "connected",
            client_id: this.client_id
        }))
    }

    sendQuery(searchQuery: HTMLInputElement) {
        const this1 = this
        return function () {
            let searchQuery = document.getElementById("userInput")! as HTMLInputElement

            const query = searchQuery.value
            this1.ws.send(JSON.stringify({
                action: "query",
                client_id: this1.client_id,
                query: query
            }))
        }
    }
}
