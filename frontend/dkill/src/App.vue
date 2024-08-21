<template>
  <div id="app">
    <el-container>
      <el-header>
        <h2>端口管理工具</h2>
      </el-header>
      <el-main>
        <port-list />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import PortList from './components/PortList.vue'

export default {
  components: {
    PortList
  }
}
</script>

<style>
#app {
  padding: 20px;
}

h2 {
  margin: 0;
  padding: 20px 0;
  text-align: center;
}
</style>
