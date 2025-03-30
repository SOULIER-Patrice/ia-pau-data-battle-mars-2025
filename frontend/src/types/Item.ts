export type Item = {
    title: string
    description?: string
    href?: string
    buttons?: {
        title: string
        onPress: () => void
        color?: string
        icon?: string
        width?: string
        height?: string
        padding?: string
    }[]
    chips?: {
        title: string
        color?: string
        bgColor?: string
    }[]
}