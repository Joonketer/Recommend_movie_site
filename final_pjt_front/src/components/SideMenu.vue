<template>
    <div class="side-menu">
        <img id="navcon" src="../assets/C.png" >
        <hr>
        <div >
            <img id="userdefaultimage" src="..//assets/defaultuserimage.png" >
            <router-link to="/:id/profile">User Profile</router-link>
            <hr>
            <router-link to="/">Home</router-link>
            <hr>
            <router-link to="/detailsearch">Detailed Search</router-link>
            <hr>
            <router-link to="/boxoffice">Box Office</router-link>
            <hr>
            <router-link to="/featured">Featured Movies</router-link>
            <hr>
            <router-link to="/community">Community</router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SideMenu'
}
</script>

<style scoped>
/* .side-menu {
} */
</style>
