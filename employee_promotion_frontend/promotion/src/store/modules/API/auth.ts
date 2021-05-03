import axios from 'axios';
import { User,UserData } from '../../models';
const conf = require('../../../config/config.js');
export const instance = axios.create({
    baseURL: conf.API_LOCATION
});

type loginReturn = {
  code: string;
  Token: string;
  "Token-refresh": string;
  success: boolean;
  expiration_date: string;
  username: string;
  user: UserData;
}
/**
 * suppresion du token pour qu'il ne soit plus valid
 * @param Token 
 */
export async function logout(Token: string): Promise<void> {
  
  await instance.delete('/login',{
      headers:{
        "Content-Type": 'application/json',
        "Authorization": 'Bearer '.concat(Token)
      }
    })
    .then(() => console.log("logout"))
    .catch(e => console.log(e));
}
/**
 * refresh le token en cas d'expiration
 * @param Token 
 */
export async function refreshToken(Token:string): Promise<void> {
  await instance.post('/refresh',
    Token)
    .then(() => console.log("refresh"))
    .catch(e => console.log(e));
}
/**
 * verification tu token de session si il est toujour valable
 * @param Token 
 */
export async function testToken(): Promise<string> {
  const Token = localStorage.getItem("Token");
  let expirationDate = "0";
  if(localStorage.getItem("expiration_date") != "") {
    expirationDate = localStorage.getItem("expiration_date") ?? "0";
  }
  const expiration = Date.parse(expirationDate);
  const diff = expiration - new Date().getTime();
  if(diff < 1 || Token == ("" || null)) {
    return "";
  }
  const response = await instance.post('/testToken',"",
    {
      headers:{
        "Content-Type": 'application/json',
        "Authorization": 'Bearer '.concat(Token)
      }
    }
  ).then(res => { return res.data.message; }).catch(e => console.log(e));
  return response;
}
export async function login(user: User): Promise<loginReturn>{
  try{
      const result:loginReturn ={
        code: "",
        Token:  "",
        success: false,
        'Token-refresh': "",
        expiration_date: "",
        username: "",
        user:{
          "email": "",
          "id": 0,
          "username": ""
        }
      };
      await instance.post('/login',
        user
      ).then((res)=>{ 
        result.code = res.data.code;
        result.Token = res.data.Token;
        result.success = res.data.success;
        result["Token-refresh"] = res.data.refresh_token;
        result.expiration_date = res.data.expiration_date;
        result.username = res.data.user.username;
        result.user = res.data.user;
        // Sentry.setUser({
        //   username: res.data.user.username,
        //   id: res.data.user.id,
        //   email: res.data.user.email
        // });
      }).catch(() => {
        // Sentry.captureException(err);
      });
      return result;
      
  } catch(e) {
    console.error(e);
    return {
      code: "",
      Token:  "",
      success: false,
      "Token-refresh": "",
      expiration_date: "",
      username: "",
      user: {
        "email": "",
        "id": 0,
        "username": ""
      }
    };
  }  
}
