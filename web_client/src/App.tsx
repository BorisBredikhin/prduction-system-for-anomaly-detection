import React from 'react';
import './App.css';
import {AppBar, Box, Toolbar, Typography} from "@mui/material";
import Search from "./components/search/search";
import SearchIconWrapper from "./components/search/search-icon-wrapper";
import SearchIcon from '@mui/icons-material/Search'
import {StyledInputBase} from "./compnens/styled-input-base";


function App() {
    return (
        <Box sx={{flexGrow: 1}}>
            <AppBar position="static">
                <Toolbar>
                    <Typography>
                        Экспертная система для определения аномалий
                    </Typography>
                </Toolbar>
            </AppBar>
            <Search onClick={console.log}/>
        </Box>
    );
}

export default App;
