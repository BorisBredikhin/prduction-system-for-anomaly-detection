import React, {useEffect, useRef, useState} from 'react';
import './App.css';
import {AppBar, Box, Toolbar, Typography} from "@mui/material";
import Search from "./components/search/search";
import {Client, Message} from "./client";

let k = false

function App() {
    const [messages, setMessages] = useState<Message[]>([])
    const [client, setClient] = useState<Client>(new Client(messages, setMessages))


    useEffect(() => {
        if (!k){
            k=true
            return
        }
        // setClient(new Client(messages, setMessages))
        
        client.ws.onopen = function () {
        client.ws.send(JSON.stringify({
            action: "connected",
            client_id: client.client_id
        }))
    }}, [client.client_id])
    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="static">
                <Toolbar>
                    <Typography>
                        Экспертная система для определения аномалий
                    </Typography>
                </Toolbar>
            </AppBar>
            <Search onClick={client.sendQuery('userInput', 'msgs')}/>
        </Box>
    );
}

export default App;
