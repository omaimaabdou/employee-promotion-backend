export interface User {
    username: string,
    token: string,
    "Token-refresh": string
    user: UserData
}

export interface UserData {
    email: string,
    id: number,
    username: string
}
export interface Employee {
    employee_uid : string,
}
