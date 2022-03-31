<template>
  <q-page class="full-width column justify-center">
    <div class="q-pa-md">
      <div class="q-gutter-y-md" style="max-width: 1600px">
        <q-card>
          <q-tabs
            v-model="tab"
            dense
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            align="justify"
            narrow-indicator
          >
            <q-tab name="Login" label="登录" />
            <q-tab name="Regis" label="注册" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated>
            <q-tab-panel class="column" name="Login">
              <q-input v-model="regForm.account" label="account" />
              <q-input
                v-model="regForm.password"
                label="password"
                type="password"
              />

              <div class="row justify-center top-margin" style="">
                <q-btn
                  class=""
                  style="margin-left: auto"
                  color="white"
                  text-color="black"
                  label="登录"
                  @click="login"
                />
                <q-btn
                  style="margin-left: auto"
                  color="white"
                  text-color="black"
                  label="忘记密码"
                  href="auth/forgotpassword"
                />
              </div>
            </q-tab-panel>

            <q-tab-panel name="Regis" class="column"
              ><q-input v-model="regForm.account" label="account" />
              <q-input
                v-model="regForm.password"
                label="password"
                type="password"
              />
              <q-input v-model="regForm.email" label="email" />
              <q-btn
                class="col self-center top-margin"
                color="white"
                text-color="black"
                label="注册"
                @click="register"
              />
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, reactive } from "vue";
import { get, post } from "boot/axios";
import { getUtils } from "boot/utils";
import { LocalStorage, SessionStorage } from "quasar";
import { useRouter } from "vue-router";
import { useStore } from "stores/bridge";
export default defineComponent({
  name: "AuthPart",
  setup() {
    const regForm = reactive({
      account: "",
      password: "",
      email: "",
    });
    const router = useRouter();
    const login = async () => {
      let res = await post(process.env.API + "auth/jwt/create/", {
        username: regForm.account,
        password: regForm.password,
      });
      if (res instanceof Error) {
        return alert("用户名/密码错误或用户未验证");
      }

      LocalStorage.set("access", res.data.access);
      LocalStorage.set("refresh", res.data.refresh);

      res = await getUtils(process.env.API + "auth/users/me/", true);
      const store = useStore();
      store.setUser({
        id: res.data.id,
        username: res.data.username,
        email: res.data.email,
      });

      res = await getUtils(process.env.API + "auth/users/me/", true);

      router.go(-1);
      // window.location.reload();
    };
    const register = async () => {
      let res = await post(process.env.API + "auth/users/", {
        username: regForm.account,
        password: regForm.password,
        email: regForm.email,
      });
      if (res instanceof Error) {
        return alert(
          "注册失败,用户名/邮箱已被使用" + JSON.stringify(res.response.data)
        );
      }

      alert("验证邮件已发送到您的邮箱，请查收");
      router.go(0);
      // window.location.reload();
    };
    return {
      regForm,
      login,
      register,
      tab: ref("Login"),
    };
  },
});
</script>
