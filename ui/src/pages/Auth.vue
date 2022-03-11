<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md" style="max-width: 600px">
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
          <q-tab name="mails" label="Mails" />
          <q-tab name="alarms" label="Alarms" />
          <q-tab name="movies" label="Movies" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="mails">
            <q-input v-model="regForm.account" label="account" />
            <q-input v-model="regForm.passwordText" label="password" />
            <q-btn
              color="white"
              text-color="black"
              label="Standard"
              @click="register"
            />
            <q-btn color="white" text-color="black" label="Standard" />
          </q-tab-panel>

          <q-tab-panel name="alarms"> </q-tab-panel>

          <q-tab-panel name="movies"> </q-tab-panel>
        </q-tab-panels>
      </q-card>

      <q-card>
        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="mails">
            <div class="text-h6">Mails</div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </q-tab-panel>

          <q-tab-panel name="alarms">
            <div class="text-h6">Alarms</div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </q-tab-panel>

          <q-tab-panel name="movies">
            <div class="text-h6">Movies</div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </q-tab-panel>
        </q-tab-panels>

        <q-separator />

        <q-tabs
          v-model="tab"
          dense
          class="bg-grey-3"
          align="justify"
          narrow-indicator
        >
          <q-tab name="mails" label="Mails" />
          <q-tab name="alarms" label="Alarms" />
          <q-tab name="movies" label="Movies" />
        </q-tabs>
      </q-card>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, reactive } from "vue";
import axios from "axios";

export default defineComponent({
  name: "Auth",
  setup() {
    const regForm = reactive({
      accountText: "",
      passwordText: "",
    });

    const register = async () => {
      const register2 = (account, password) => {
        axios.post("http://127.0.0.1:3333/api/auth/register", {
          account,
          password,
        });
      };
      const res = await register2(regForm.account, regForm.password);
      console.log(res);
    };
    return {
      regForm,
      register,
      tab: ref("mails"),
    };
  },
});
</script>
