<template>
  <q-page class="fit row wrap justify-start items-start content-start">
    <q-list bordered separator class="content-center col-9">
      <q-item v-ripple v-for="(i, index) in dynamics" :key="index">
        <q-item-section>
          <q-item-label v-show="i[comment]"
            >{{ i.username }}于{{ i.time }}参与了讨论{{
              i.discuss
            }}</q-item-label
          >
          <q-item-label v-show="!i[comment]"
            >{{ i.username }}于{{ i.time }}发布了讨论{{
              i.discuss
            }}</q-item-label
          >
        </q-item-section>
      </q-item>
    </q-list>
    <q-list bordered separator class="content-center col-3">
      <div style="padding: 25px">
        <q-avatar size="100px" class="offset-1">
          <img :src="avatar" />
        </q-avatar>
      </div>
      <q-item v-ripple>
        <q-item-section>
          <q-item-label overline>昵称</q-item-label>
          <q-item-label>{{ username }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item v-ripple>
        <q-item-section>
          <q-item-label overline>简介</q-item-label>
          <q-item-label>{{ introduce }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item v-ripple>
        <q-item-section>
          <q-item-label overline>生日</q-item-label>
          <q-item-label>{{ birthday }}</q-item-label>
        </q-item-section>
      </q-item>
      <q-item v-ripple>
        <q-item-section>
          <q-item-label overline>邮箱</q-item-label>
          <q-item-label>{{ email }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-page>
</template>

<script>
import { defineComponent, ref, reactive, onBeforeMount } from "vue";
import { getUtils } from "boot/utils";
import { useStore } from "stores/bridge";
import { useRoute } from "vue-router";

export default defineComponent({
  name: "UserData",

  setup() {
    const username = ref();
    const email = ref();
    const avatar = ref();
    const introduce = ref();
    const birthday = ref();
    const store = useStore();
    const route = useRoute();
    const dynamics = ref();
    username.value = route.params.username;
    getUtils(process.env.API + "wu/userinfos/" + username.value, false).then(
      (res) => {
        email.value = res.data.email;
        avatar.value = res.data.avatar;
        introduce.value = res.data.introduce;
        birthday.value = res.data.birthday;
      }
    );
    // getUtils(process.env.API + "wu/dynamic/", false, {
    //   username: username.value,
    // }).then((res) => {
    //   dynamics.value = res.data.results;
    // });
    getUtils(
      process.env.API + "wu/dynamic/" + username.value + "/",
      false
    ).then((res) => {
      dynamics.value = res.data.data;
    });

    return {
      dynamics,
      username,
      email,
      avatar,
      introduce,
      birthday,
    };
  },
});
</script>
