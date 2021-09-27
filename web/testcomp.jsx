import Button from '@mui/material/Button';

export default function CustomButton({text}) {
  return (
    <Button variant="contained" disableElevation color="blue">
      {text}
    </Button>
  );
}

<CustomButton text="Hello"></CustomButton>
