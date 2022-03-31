<template>
  <q-page class="column">
    <div class="q-gutter-lg all-padding">
      <q-input
        v-model="new_password"
        filled
        :type="isPwd1 ? 'password' : 'text'"
        hint="请输入新密码"
      >
        <template v-slot:append>
          <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
          />
        </template>
      </q-input>
      <q-input
        v-model="re_new_password"
        filled
        :type="isPwd2 ? 'password' : 'text'"
        hint="请重复新密码"
      >
        <template v-slot:append>
          <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
          />
        </template>
      </q-input>
      <div>
        <q-btn
          class="full-width"
          color="white"
          text-color="black"
          label="确认"
          @click="modify"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, reactive, watch } from "vue";
import { getUtils, postUtils, putUtils, patchUtils } from "boot/utils";
import { LocalStorage, SessionStorage } from "quasar";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "stores/bridge";
import { compress, compressAccurately } from "image-conversion";

export default defineComponent({
  name: "ForgotPasswordConfirm",

  setup() {
    const store = useStore();

    const route = useRoute();
    const uid = ref(route.params.uid);
    const token = ref(route.params.token);
    const new_password = ref();
    const re_new_password = ref();

    return {
      async modify() {
        let res = await postUtils(
          process.env.API + "auth/users/reset_password_confirm/",
          {
            uid: uid.value,
            token: token.value,
            new_password: new_password.value,
            re_new_password: re_new_password.value,
          }
        );
        if (res instanceof Error) {
          alert(res.response.data);
        } else {
          alert("重置密码成功");
        }
      },
      new_password,
      re_new_password,
      isPwd1: ref(true),
      isPwd2: ref(true),
    };
  },
});
</script>
<!-- <style lang = "scss" scoped>
  @import "../assets/style/common.scss";
</style> -->
