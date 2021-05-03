import { VuexModule, Module, Mutation,getModule} from 'vuex-module-decorators';
import store

@Module({
    namespaced: true,
    dynamic: true,
    name: 'app',
    store,
    preserveState: localStorage.getItem('vuex') !== null,
})

class AppModule extends VuexModule {
    currentPage = "";

    @Mutation
    setCurrentPage(value: string) {
        this.currentPage = value;
    }
}
export default getModule(AppModule);
