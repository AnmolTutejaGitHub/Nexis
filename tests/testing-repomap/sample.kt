import java.util.LinkedList
import kotlin.math.max

data class Config(val host: String, val port: Int, val maxConnections: Int = 10)

interface Pool<T> {
    fun acquire(): T?
    fun release(item: T)
    val size: Int
}

class ConnectionPool(private val config: Config) : Pool<String> {
    private val pool = LinkedList<String>()

    override fun acquire(): String? = pool.poll()
    override fun release(item: String) { pool.add(item) }
    override val size get() = pool.size

    fun resize(newMax: Int): ConnectionPool {
        return ConnectionPool(config.copy(maxConnections = max(newMax, 1)))
    }
}

object DatabaseManager {
    private var instance: ConnectionPool? = null

    fun getInstance(config: Config): ConnectionPool {
        return instance ?: ConnectionPool(config).also { instance = it }
    }

    fun connect(url: String): Boolean = url.isNotBlank()
}

fun parseUrl(url: String): Config {
    val parts = url.split(":")
    return Config(host = parts[0], port = parts.getOrNull(1)?.toIntOrNull() ?: 5432)
}
