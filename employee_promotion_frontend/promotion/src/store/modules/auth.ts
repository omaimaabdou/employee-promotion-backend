import { VuexModule, Module, Action, Mutation,getModule } from 'vuex-module-decorators';
import store from '../../store'
import {User} from '../models';
import { auth } from './api';

@Module({
  namespaced: true,
  dynamic: true,
  name: 'auth',
  store,
  preserveState: localStorage.getItem('vuex') !== null,
})

class AuthsModule extends VuexModule {
  user!: User


  get isAuthenticated() {
    return !!this.user?.token;
  }

  @Mutation
  setUser(user: User){
    this.user = user;
  }
  @Action({commit: 'setUser', rawError: true})
  async login(userLogin: any): Promise<any> {
    const result = await auth.login(userLogin);
    if (result?.success) {
      localStorage.setItem("Token", result.Token);
      localStorage.setItem("Token-refresh", result["Token-refresh"]);
      localStorage.setItem("expiration_date", result["expiration_date"]);
      const user = {
        username : result.username,
        token: result.Token,
        "Token-refresh": result["Token-refresh"],
        user: result.user
      };
      return user;
    }
    return false;
  }
  /**
   * Deconnection
   */
  @Action({ commit: 'setUser',rawError: true  })
    async logout() {
    // @ts-ignore
    auth.logout(store.state.auth.user.token);
    localStorage.removeItem("Token");
    localStorage.removeItem("Token-refresh");
    localStorage.removeItem("expiration_date");
    return null;
  }
  /**
   * Rafreshir le token
   */
  @Action
  async refreshToken() {
    // @ts-ignore
    const Token = await auth.refreshToken(store.state.auth.user.token);
    return Token != null;
  }
  /**
   * Tester si le token et toujour valable ou non
   */
  @Action
  async testToken() {
    const test = await auth.testToken();
    return test == "OK";
  }
}

export default getModule(AuthsModule);
