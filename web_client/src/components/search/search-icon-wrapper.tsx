import {styled} from "@mui/material";

export default styled('div')(({ theme }) => ({
    padding: theme.spacing(0, 0, 0, 0),
    // height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',

}));
