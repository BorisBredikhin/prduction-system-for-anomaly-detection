import {alpha, Button, Input, InputAdornment, styled} from "@mui/material";
import SearchIcon from "@mui/icons-material/Send";
import React, {MouseEventHandler} from "react";

const SearchStyleDiv = styled('div')(({theme}) => ({
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
        backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
        marginLeft: theme.spacing(1),
        width: 'auto',
    },
}));


export interface SearchProps {
    onClick: MouseEventHandler
}

const Search = (props: SearchProps) => <SearchStyleDiv>
    <Input
        id="userInput"
        autoFocus
        onKeyDown={function (event) {
            if (event.key == 'Enter')
                props.onClick(undefined!)
        }}
        placeholder="Введите запрос"
        endAdornment={
            <InputAdornment position="end">
                <Button onClick={props.onClick}>
                    <SearchIcon/>
                </Button>
            </InputAdornment>
        }
    />
</SearchStyleDiv>

export default Search;
