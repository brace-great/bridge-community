<template>
  <q-page class="fit row wrap justify-start items-start content-start">
    <q-list bordered separator class="content-center col-12">
      <q-item v-ripple v-for="(i, index) in data" :key="index">
        <q-item-section>
          <q-item-label
            >{{ i.from_who }}{{ i.event_type + "     "
            }}{{ i.time }}</q-item-label
          >
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
  name: "UserNotify",

  setup() {
    const store = useStore();
    const route = useRoute();
    const data = ref();
    const username = store.user.username;

    onBeforeMount(async () => {
      data.value = store.notify;
      for (const i in data.value) {
        if (data.value[i].event_type == 1) {
          data.value[i].event_type =
            "参与了你发布的讨论" + data.value[i].discuss_title;
        } else if (data.value[i].event_type == 2) {
          data.value[i].event_type =
            "于讨论" + data.value[i].discuss_title + "中回复了你";
        }
      }
    });

    return { data };
  },
});
</script>
