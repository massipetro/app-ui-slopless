// A debug app that holds one generated screen, opened through ui-tooling's PreviewActivity.
// Same library versions as scripts/kotlin-check, so what compiled there renders here.
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    // The build's own package, so its `import <package>.R` resolves. applicationId stays fixed.
    namespace = (findProperty("slopless.namespace") as String?) ?: "dev.slopless.render"
    compileSdk = 36
    defaultConfig {
        applicationId = "dev.slopless.render"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1"
    }
    buildFeatures { compose = true }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    sourceSets["main"].java.srcDirs("src/main/kotlin")
}

kotlin {
    compilerOptions { jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17) }
}

dependencies {
    val compose = "1.9.0"
    implementation("androidx.activity:activity-compose:1.10.1")
    implementation("androidx.core:core-ktx:1.16.0")
    implementation("androidx.compose.ui:ui:$compose")
    implementation("androidx.compose.ui:ui-tooling:$compose")
    implementation("androidx.compose.ui:ui-tooling-preview:$compose")
    implementation("androidx.compose.ui:ui-text-google-fonts:$compose")
    implementation("androidx.compose.foundation:foundation:$compose")
    implementation("androidx.compose.animation:animation:$compose")
    implementation("androidx.compose.material3:material3:1.4.0")
    implementation("androidx.compose.material:material-icons-extended:1.7.8")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.9.1")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.9.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.2")
    implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.6.2")
    implementation("io.coil-kt.coil3:coil-compose:3.1.0")
}
