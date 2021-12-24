import React, {useEffect, useRef, useState} from 'react';
import './App.css';
import {AppBar, Box, Toolbar, Typography} from "@mui/material";
import Search from "./components/search/search";
import {Client} from "./client";

const client = new Client()

function App() {
    const [messages, setMessages] = useState<string[]>([])

    useEffect(() => client.ws.onopen = function () {
        client.ws.send(JSON.stringify({
            action: "connected",
            client_id: client.client_id
        }))
    })
    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="static">
                <Toolbar>
                    <Typography>
                        Экспертная система для определения аномалий
                    </Typography>
                </Toolbar>
            </AppBar>
            <div id='msgs'>Оправьте любое сообщение, чтобы начать</div>
            <Search onClick={client.sendQuery('userInput', 'msgs')}/>
        </Box>
    );
}

export default App;
