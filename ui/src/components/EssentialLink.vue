<template>
  <q-item clickable tag="a" target="_self" :to="link">
    <q-item-section v-if="icon" avatar>
      <q-icon :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label>{{ title }}</q-item-label>
      <q-item-label caption>{{ caption }}</q-item-label>
    </q-item-section>
    <q-item-section>
      <div class="row reverse">
        <q-badge rounded color="red" :label="badge" v-if="badge" />
      </div>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent, reactive, watchEffect, toRefs } from "vue";

export default defineComponent({
  name: "EssentialLink",
  // methods: {
  //   changeBadge(newVal) {
  //     badge = newVal;
  //     console.log("badge", badge);
  //   },
  // },

  props: {
    title: {
      type: String,
      required: true,
    },

    caption: {
      type: String,
      default: "",
    },

    link: {
      type: String,
      default: "#",
    },

    icon: {
      type: String,
      default: "",
    },
    badge: {
      type: [Number, null, Object],
      default: null,
    },
  },
  setup(props) {
    const state = reactive({
      badge: "",
    });
    watchEffect(() => {
      state.badge = props.badge;
    });
    return {
      ...toRefs(state),
    };
  },
});
</script>
