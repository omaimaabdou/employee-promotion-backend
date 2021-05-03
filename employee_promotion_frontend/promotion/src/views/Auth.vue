<template>
  <div class="w-100 d-flex flex-column justify-content-between vh-100">
    <div class="text-center d-flex flex-column justify-content-center">
      <div class="row">
        <div class="col"></div>
        <div
          class="col d-flex flex-column justify-content-center align-items-center"
        >
          <img
            src="@/assets/logo.png"
            alt="Logo Derush"
            style="width: auto; height: 60px; object-fit: cover"
          />
        </div>
      </div>
      <!-- <brutalism-title subtitle="Extension" /> -->
      <span
        id="normal"
        style="font-size: 12px; font-weight: bold"
        class="text-center mb-5 mx-auto"
        >{{ $t("message.auth.title") }}</span
      >
      <div class="w-50 mx-auto">
        <div class="d-flex flex-column align-items-center">
          <input
            class="form-control mb-2"
            type="text"
            :placeholder="$t('message.auth.username')"
            v-model="username"
          />
          <input
            class="form-control mb-2"
            type="password"
            :placeholder="$t('message.auth.password')"
            v-model="password"
            inputType="password"
            @keypress.enter="login"
          />
        </div>
        <div class="d-flex justify-content-center">
          <button
            type="submit"
            @click="login"
            v-promise-btn
            class="btn btn-light w-100"
          >
            {{ $t("message.auth.login") }}
          </button>
        </div>
        <div class="mt-3">
          <span class="d-block text-danger error mx-auto" v-if="errorAuth">{{
            $t("message.auth.invalid")
          }}</span>
          <router-link to="/forgot-password" class="text-white forgot">{{
            $t("message.auth.forgot")
          }}</router-link>
        </div>

        <div class="d-flex justify-content-between mt-4 mx-5">
          <div></div>
          <div class="d-flex align-items-center justify-content-center ml-5">
            <span class="mb-0">{{ $t("message.auth.first_time") }} </span>
            <span class="mdi mdi-arrow-right ml-3"></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Component, Watch } from "vue-property-decorator";
import AuthsModule from "../store/modules/auth";
import axios from 'axios';

const conf = require('../config/config');
const AuthInstance = AuthsModule;

@Component({})
export default class Home extends Vue {
  username = "";
  password = "";
  errorAuth = false;

  async login() {
    if (this.username == "" || this.password == "") {
      alert(`${this.$t("message.auth.empty_inputs")}`);
    } else {
      AuthInstance.login({
        username: this.username,
        password: this.password,
      })
        .then(async (res: any) => {
          if (res) {
            let token = window.localStorage.getItem("Token"); 
            this.$router.push("/");
            
          } else {
            this.errorAuth = true;
          }
        })
        .catch((err: any) => {
          this.errorAuth = true;
        });
    }
  }
}
</script>

<style lang="scss" scoped>
.faq-button {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #c4c4c4;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    text-decoration: none !important;
    &:hover {
      cursor: pointer;
    }
    .stop-emoji {
      font-size: 2em;
    }
  }
</style>
