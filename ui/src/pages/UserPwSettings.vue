<template>
  <q-page class="column">
    <div class="q-gutter-lg all-padding">
      <q-input
        v-model="oldPw"
        filled
        :type="isPwd ? 'password' : 'text'"
        hint="请输入旧密码"
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
        v-model="newPw"
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
        v-model="repeat"
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
          label="保存"
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
import { useRouter } from "vue-router";
import { useStore } from "stores/bridge";
import { compress, compressAccurately } from "image-conversion";

export default defineComponent({
  name: "UserPwSettings",

  setup() {
    const store = useStore();
    const username = store.user.username;
    const oldPw = ref();
    const newPw = ref();
    const repeat = ref();

    return {
      async modify() {
        let res = await postUtils(
          process.env.API + "auth/users/set_password/",
          {
            new_password: repeat.value,
            re_new_password: newPw.value,
            current_password: oldPw.value,
          },
          true
        );
        if (res instanceof Error) {
          alert("原密码错误");
        } else {
          alert("修改成功");
        }
      },
      oldPw,
      newPw,
      repeat,
      isPwd: ref(true),
      isPwd1: ref(true),
      isPwd2: ref(true),
    };
  },
});
</script>
<!-- <style lang = "scss" scoped>
  @import "../assets/style/common.scss";
</style> -->
