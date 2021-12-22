import React, {useEffect, useRef} from 'react';
import './App.css';
import {AppBar, Box, Toolbar, Typography} from "@mui/material";
import Search from "./components/search/search";
import {Client} from "./client";

const client = new Client()

function App() {
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
            <Search onClick={client.sendQuery(document.querySelector('#root > div > div > div > input')!)}/>
        </Box>
    );
}

export default App;
