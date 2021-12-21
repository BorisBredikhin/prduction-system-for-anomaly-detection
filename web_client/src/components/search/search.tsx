import {alpha, Input, InputAdornment, styled} from "@mui/material";
import SearchIconWrapper from "./search-icon-wrapper";
import SearchIcon from "@mui/icons-material/Search";
import {StyledInputBase} from "../../compnens/styled-input-base";
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
    onClick: MouseEventHandler;
}

const Search = (props: SearchProps) => <SearchStyleDiv>
    <Input
        id="userInput"
        placeholder="Введите запрос"
        endAdornment={
            <InputAdornment position="end">
                <SearchIcon onClick={props.onClick}/>
            </InputAdornment>
        }
    />
</SearchStyleDiv>

export default Search;
