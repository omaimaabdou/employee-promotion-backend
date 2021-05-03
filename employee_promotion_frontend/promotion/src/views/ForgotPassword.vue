<template>
  <div id="forgot-password" class="vh-100">
    <div class="row">
      <div class="col">
        <router-link
          to="/login"
          class="d-inline-flex align-items-center decoration-none text-white"
        >
          <span class="mdi mdi-chevron-left"></span>
          <span class="logout-emoji">🔑</span>
        </router-link>
      </div>
      <div class="col">
        
      </div>
      <div class="col"></div>
    </div>
    <p
      style="font-size: 12px; font-weight: bold"
      class="text-center mb-1 mx-auto"
      >{{ $t("message.password_recovery.title") }}</p
    >
    <div v-if="sendEmail" class="container mt-4">
      <input
        :placeholder="$t('message.password_recovery.email')"
        v-model="email"
        class="w-100"
      />
      <div
        class="mt-4 d-flex flex-column justify-content-center align-items-center"
      >
        <button type="button" class="submit-btn" v-promise-btn @click="send">
          {{ $t("message.password_recovery.send") }}
        </button>
        <p class="mt-3" v-if="emailSent">Email has been sent</p>
        <p class="text-danger mt-3" v-if="emailError">{{
          emailErrorMsg
        }}</p>
      </div>
    </div>
    <div v-if="!sendEmail" class="container mt-4">
      <input
        :placeholder="$t('message.password_recovery.code')"
        v-model="code"
        class="w-100 mb-4"
        filled
      />
      <input
        :placeholder="$t('message.password_recovery.new_password')"
        v-model="password"
        type="password"
        class="w-100"
        filled
      />
      <div
        class="mt-4 d-flex justify-content-cener flex-column align-items-center"
      >
        <button type="button" class="submit-btn" v-promise-btn @click="update">
          {{ $t("message.password_recovery.update") }}
        </button>
        <Anno class="text-danger mt-3" v-if="updateError">{{ errorMsg }}</Anno>
      </div>
    </div>
  </div>
</template>

<script lang=ts>
import { Component } from "vue-property-decorator";
import Vue from "vue";
import axios from "axios";
// import * as Sentry from "@sentry/vue";
const conf = require("../config/config");

@Component({})
export default class ForgotPassword extends Vue {
  email: string = "";
  code: string = "";
  password: string = "";
  emailSent: boolean = false;
  sendEmail: boolean = true;
  emailError: boolean = false;
  updateError: boolean = false;
  updated: boolean = false;
  emailErrorMsg: string = "";
  errorMsg: string = "";

  async send() {
    await axios
      .post(`${conf.API_LOCATION}/forgot`, {
        email: this.email,
      })
      .then((res) => {
        this.sendEmail = false;
        this.emailSent = true;
        this.emailError = false;
      })
      .catch((err: any) => {
        // Sentry.captureException(err);
        let data = err.response.data;
        this.emailError = true;
        if(data.error.code == 102) {
          this.emailErrorMsg = this.$t('message.password_recovery.error_email').toString();
        }else {
          this.emailErrorMsg = data.error.message;
        }
      })
      .finally(() => {
        document.querySelector(".panel")?.scrollBy(0, 1000);
      });
  }

  async update() {
    await axios
      .post(`${conf.API_LOCATION}/reset`, {
        email: this.email,
        token: this.code,
        password: this.password,
      })
      .then(async (res) => {
        this.updated = true;
        this.updateError = false;
        alert(`${this.$t("message.password_recovery.success")}`);
        this.$router.push("/login");
      })
      .catch((err: any) => {
        // Sentry.captureException(err);
        let data = err.response.data;
        this.updateError = true;
        if(data.error.code == 102) {
          this.errorMsg = this.$t('message.password_recovery.error_email').toString();
        } else if(data.error.code == 115) {
          this.errorMsg = this.$t('message.password_recovery.incorrect_token').toString();
        }else {
          this.errorMsg = data.error.message;
        }
      })
      .finally(() => {
        document.querySelector(".panel")?.scrollBy(0, 1000);
      });
  }
}
</script>

<style lang="scss">
#forgot-password {
  .mdi {
    font-size: 24px;
  }
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
  input {
    background-color: #b1b1b1 !important;
    border-radius: 20px !important;
    border: none;
    outline: none;
    height: 40px;
    padding-left: 18px !important;
    padding-right: 18px !important;
  }
  .input-inside.filled,
  .input-inside:focus,
  .input-inside.filled.active {
    border: none !important;
    outline: none !important;
    background: none !important;
  }
  .input-label,
  label,
  .textarea-label,
  .select-label {
    color: white;
    margin-bottom: 8px;
    margin-left: 18px;
    top: -8px;
  }
  .submit-btn {
    width: 173px;
    height: 35px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
    background-color: #ffffff;
    color: #000000;
    font-size: 16px;
    font-weight: bold;
    border-radius: 20px;
    border: none;
  }
  .decoration-none {
    text-decoration: none;
  }
}
</style>
