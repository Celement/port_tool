<template>
  <div>
    <el-input v-model="search" placeholder="搜索端口..." style="margin-bottom: 20px;" clearable />
    <el-table :data="filteredPorts" style="width: 100%">
      <el-table-column prop="pid" label="PID" width="180" />
      <el-table-column prop="port" label="端口" width="180" />
      <el-table-column prop="state" label="状态" width="180" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button
            type="danger"
            size="mini"
            @click="killPort(scope.row.pid)"
          >
            终止
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'

export default {
  setup() {
    const ports = ref([])
    const search = ref('')

    const filteredPorts = computed(() => {
      return ports.value.filter(port => port.port.includes(search.value))
    })

    const fetchPorts = async () => {
      const response = await axios.get('http://127.0.0.1:5000/api/ports')
      ports.value = response.data
    }

    const killPort = async (pid) => {
      try {
        await ElMessageBox.confirm(
          `确定要终止PID为 ${pid} 的进程吗？`,
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        const response = await axios.post('http://127.0.0.1:5000/api/kill', { pid })
        ElMessage({
          message: response.data.message,
          type: response.data.status === 'success' ? 'success' : 'error',
        })
        fetchPorts()
      } catch (err) {
        if (err !== 'cancel') {
          ElMessage({
            message: '操作失败，请重试。',
            type: 'error',
          })
        }
      }
    }

    onMounted(fetchPorts)

    return {
      search,
      filteredPorts,
      killPort
    }
  }
}
</script>

<style scoped>
.el-table {
  margin-top: 20px;
}

.el-input {
  width: 300px;
}
</style>
