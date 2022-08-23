export const ItemTypes = {
  TIGER: "tiger",
  GOAT: "goat",
};

const getAPIConfig = () => {
  return {
    API_HOST: "http://localhost:8080",
    C_HOST: "http://localhost:3000",
  };
};

const configs = getAPIConfig();
export default configs;
