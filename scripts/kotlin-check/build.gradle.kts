// Compile-only harness for generated Jetpack Compose / Compose Multiplatform screens.
// commonMain code must compile for both targets (JVM and Android), so Android-only APIs
// in shared code fail here as they would in a real CMP module.
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

val withAndroid = (findProperty("slopless.android") as String?) != "false"
val resPackage = (findProperty("slopless.resPackage") as String?) ?: "kotlincheck.generated.resources"
val androidNamespace = (findProperty("slopless.namespace") as String?) ?: "dev.slopless.kotlincheck"

plugins {
    kotlin("multiplatform") version "2.2.21"
    id("org.jetbrains.kotlin.plugin.compose") version "2.2.21"
    id("org.jetbrains.compose") version "1.9.0"
    id("com.android.library") version "8.12.0" apply false
}

if (withAndroid) apply(plugin = "com.android.library")

kotlin {
    jvm {
        compilerOptions { jvmTarget.set(JvmTarget.JVM_17) }
    }
    if (withAndroid) {
        androidTarget {
            compilerOptions { jvmTarget.set(JvmTarget.JVM_17) }
        }
    }
    sourceSets {
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.runtimeSaveable)
            implementation(compose.components.uiToolingPreview)
            implementation(compose.foundation)
            implementation("org.jetbrains.compose.material3:material3:1.9.0")
            implementation(compose.materialIconsExtended)
            implementation(compose.ui)
            implementation(compose.animation)
            implementation(compose.components.resources)
            implementation("org.jetbrains.androidx.lifecycle:lifecycle-runtime-compose:2.9.1")
            implementation("org.jetbrains.androidx.lifecycle:lifecycle-viewmodel-compose:2.9.1")
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.2")
            implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.6.2")
            implementation("io.coil-kt.coil3:coil-compose:3.1.0")
        }
        if (withAndroid) {
            androidMain.dependencies {
                implementation("androidx.activity:activity-compose:1.10.1")
                implementation("androidx.compose.ui:ui-tooling-preview:1.9.0")
                implementation("androidx.compose.ui:ui-text-google-fonts:1.9.0")
                implementation("androidx.core:core-ktx:1.16.0")
            }
        }
    }
}

if (withAndroid) {
    extensions.configure<com.android.build.gradle.LibraryExtension>("android") {
        namespace = androidNamespace
        compileSdk = 36
        defaultConfig { minSdk = 24 }
        compileOptions {
            sourceCompatibility = JavaVersion.VERSION_17
            targetCompatibility = JavaVersion.VERSION_17
        }
    }
}

compose.resources {
    publicResClass = true
    packageOfResClass = resPackage
    generateResClass = always
}
